"""
continuous.py
=============

真·连续批处理（continuous batching）——推理优化 Step 4 的进阶。

与 ``serving.py`` 的 lockstep 静态批处理不同，本引擎：
- 每个请求拥有**独立的 KV 缓存**，batch 内长度可不同（靠 per-row 掩码 / padded 前向）；
- **动态 slot 复用**：某个请求提前结束（达到 max_new / 遇到 EOS）时，
  立即把它的位置让给队首的新请求，让 batch 始终满载。

这让请求长度**参差不齐**时也能保持高吞吐——这正是 vLLM / TGI 等 serving
框架的核心机制。PagedAttention 则进一步把 KV 按固定块(block)分配以省显存，
本实现用按请求 padded 的 KV 缓存演示 slot 复用语义。
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import torch

from llm.gpt import GPT


@dataclass
class Slot:
    """一个进行中的请求（占用一个 batch 位置）。"""

    req_id: int
    prompt: torch.Tensor
    max_new: int
    pads: list = field(default_factory=list)  # 每层 (K, V) 填充缓存
    cache_len: int = 0
    last_tok: torch.Tensor | None = None
    output: list = field(default_factory=list)
    out_count: int = 0


def _prefill_slot(model: GPT, slot: Slot, buffer_len: int) -> None:
    """把请求 prefill 进 slot：填充 KV、产出第一个 token。"""
    model.eval()
    with torch.no_grad():
        cache_lens = torch.zeros(1, dtype=torch.long, device=slot.prompt.device)
        logits, pads = model.forward_continuous(
            slot.prompt, None, cache_lens, buffer_len=buffer_len
        )
    slot.pads = pads
    slot.cache_len = slot.prompt.size(1)
    slot.last_tok = logits[:, -1:].argmax(dim=-1)
    slot.output = [slot.last_tok]
    slot.out_count = 1


class ContinuousBatchingEngine:
    """动态 slot 复用的连续批处理引擎。"""

    def __init__(self, model: GPT, max_batch: int):
        self.model = model
        self.max_batch = max_batch

    @torch.no_grad()
    def serve(self, requests):
        """
        Args:
            requests: list[tuple[prompt_tensor, max_new]]。prompt (1,T)。
        Returns:
            dict[int, torch.Tensor]：req_id -> 生成的 (1, n) token。
        """
        model = self.model.eval()
        queue = deque(requests)
        slots: list[Slot] = []
        results: dict[int, torch.Tensor] = {}

        # KV 缓冲区按需分配：最长 prompt + 最长生成
        buffer_len = (
            max((p.size(1) + m for p, m in requests)) if requests else self.model.config.block_size
        )

        # 填满初始 batch
        while len(slots) < self.max_batch and queue:
            prompt, max_new = queue.popleft()
            slot = Slot(req_id=len(results) + len(slots), prompt=prompt, max_new=max_new)
            _prefill_slot(model, slot, buffer_len)
            slots.append(slot)

        n_layer = len(model.transformer.h)
        while slots:
            last_toks = torch.cat([s.last_tok for s in slots], dim=0)  # (B,1)
            cache_lens = torch.tensor([s.cache_len for s in slots], dtype=torch.long)
            pads_batch = [
                (
                    torch.cat([s.pads[l][0] for s in slots], dim=0),
                    torch.cat([s.pads[l][1] for s in slots], dim=0),
                )
                for l in range(n_layer)
            ]

            logits, new_pads = model.forward_continuous(last_toks, pads_batch, cache_lens)
            next_tok = logits[:, -1:].argmax(dim=-1)  # (B,1)

            for i, s in enumerate(slots):
                s.output.append(next_tok[i : i + 1])
                s.cache_len += 1
                s.last_tok = next_tok[i : i + 1]
                s.out_count += 1
                s.pads = [
                    (new_pads[l][0][i : i + 1], new_pads[l][1][i : i + 1]) for l in range(n_layer)
                ]

            # 回收完成的 slot，动态补入新请求
            for i in reversed(range(len(slots))):
                s = slots[i]
                if s.out_count >= s.max_new:
                    results[s.req_id] = torch.cat(s.output, dim=1)
                    if queue:
                        prompt, max_new = queue.popleft()
                        new_slot = Slot(
                            req_id=len(results) + len(slots) - 1, prompt=prompt, max_new=max_new
                        )
                        _prefill_slot(model, new_slot, buffer_len)
                        slots[i] = new_slot
                    else:
                        slots.pop(i)

        return results
