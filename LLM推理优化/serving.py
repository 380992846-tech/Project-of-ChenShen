"""
serving.py
==========

批量/并发解码引擎 —— 推理优化 Step 4。

思路
----
把多个请求合成一个 batch，**每步只做一次 batched 前向**（配合每请求的 KV Cache），
从而摊销单步前向的固定开销，提升整体吞吐。

本实现采用 **lockstep 批量解码**：一个 wave 内的请求同步推进、长度一致，
因此整个 batch 共享同一 KV 缓存长度，可一次前向处理。相比逐请求串行推理，
批处理在 CPU/小模型上能明显提升吞吐（代价是单请求延迟略升——吞吐-延迟权衡）。

说明
----
真实 serving（vLLM / TGI）进一步做 **continuous batching**：某个请求提前结束时
立即把它的位置让给新请求（动态 slot 复用）。本模块用 lockstep 演示批量收益，
continuous batching 可在其基础上扩展。
"""

from __future__ import annotations

import torch

from gpt import GPT


@torch.no_grad()
def batched_generate(
    model: GPT,
    prompts: torch.Tensor,
    gen_len: int,
    sample: bool = False,
    temperature: float = 1.0,
) -> torch.Tensor:
    """
    批量生成。prompts: (B, T_prompt)，返回 (B, gen_len)。

    所有请求同步推进（lockstep），batch 内共享同一 KV 缓存长度。
    """
    model.eval()
    B, T = prompts.shape
    seq = prompts.clone()

    # prefill：一次前向处理整个 batch
    logits, past = model(seq, None)

    out: list[torch.Tensor] = []
    for _ in range(gen_len):
        input_ids = seq[:, -1:]
        logits, past = model(input_ids, past)
        logits = logits[:, -1, :] / temperature
        if sample:
            next_tok = torch.multinomial(torch.softmax(logits, dim=-1), 1)
        else:
            next_tok = logits.argmax(dim=-1, keepdim=True)
        out.append(next_tok)
        seq = torch.cat([seq, next_tok], dim=1)

    return torch.cat(out, dim=1)
