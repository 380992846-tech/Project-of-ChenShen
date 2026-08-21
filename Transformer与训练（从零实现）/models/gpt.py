"""models/gpt.py — decoder-only GPT（从零实现，自包含）

本模块与仓库 `LLM推理优化/gpt.py` 同源，复制到本项目内以保证子项目自包含、
不依赖其他目录。实现要点：

- **decoder-only 因果 Transformer**：Embedding → 多层 Block → LayerNorm → lm_head；
- **KV Cache**：解码时缓存每层 K/V，避免每步重算整个上下文；
- **权重绑定**：输入 embedding 与输出头共享权重。

用法示例::

    from models.gpt import GPT, GPTConfig

    cfg = GPTConfig(vocab_size=256, n_layer=4, n_head=4, n_embd=128)
    model = GPT(cfg)
    prompt = torch.randint(0, 256, (1, 32))
    out = model.generate(prompt, max_new_tokens=50, sample=False)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

# 每个 Block 的 attention 返回值：``(输出, 该层的 (K, V))``
PastKeyValue = tuple[torch.Tensor, torch.Tensor]


@dataclass
class GPTConfig:
    """模型超参数。"""

    vocab_size: int = 256
    n_layer: int = 4
    n_head: int = 4
    n_embd: int = 128
    block_size: int = 256
    dropout: float = 0.0


class CausalSelfAttention(nn.Module):
    """带 KV Cache 支持的因果多头自注意力。"""

    def __init__(self, config: GPTConfig):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.head_dim = config.n_embd // config.n_head

        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.dropout = nn.Dropout(config.dropout)

        # 因果下三角掩码（prefill / 全序列前向时使用）。
        # persistent=False：该 buffer 由固定规则(tril)决定，不进 state_dict，
        # 模型每次构造时都会重新注册——因此加载 checkpoint 后它依然存在，安全。
        # 同时 .to(device) 会自动迁移它，无需手动管理。
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(config.block_size, config.block_size)).view(
                1, 1, config.block_size, config.block_size
            ),
            persistent=False,
        )

    def forward(self, x: torch.Tensor, layer_past: PastKeyValue | None = None):
        """
        Args:
            x: (B, T, n_embd)。prefill 时 T=prompt 长度；decode 时 T=1。
            layer_past: 该层缓存的 (K, V)，shape (B, n_head, T_cache, head_dim)。

        Returns:
            (y, (k, v))：注意力输出，以及本层更新后的 (K, V) 缓存。
        """
        B, T, C = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)

        head = self.n_head
        hd = self.head_dim
        q = q.view(B, T, head, hd).transpose(1, 2)
        k = k.view(B, T, head, hd).transpose(1, 2)
        v = v.view(B, T, head, hd).transpose(1, 2)

        # 拼接历史 K/V（KV Cache 的核心）
        if layer_past is not None:
            past_k, past_v = layer_past
            k = torch.cat([past_k, k], dim=2)
            v = torch.cat([past_v, v], dim=2)

        T_total = k.size(2)  # 当前键的个数（含缓存）
        cache_len = T_total - T  # prefill 时 cache_len=0；decode 时 = 历史长度

        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(hd))

        if cache_len == 0:
            att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        elif T > 1:
            rows = torch.arange(T, device=x.device).view(T, 1)
            cols = torch.arange(T_total, device=x.device).view(1, T_total)
            causal = (cols <= (cache_len + rows)).view(1, 1, T, T_total)
            att = att.masked_fill(~causal, float("-inf"))

        att = F.softmax(att, dim=-1)
        att = self.dropout(att)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.c_proj(y)
        return y, (k, v)


class Block(nn.Module):
    """Transformer Block：LayerNorm → 注意力 → MLP，带残差。"""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.GELU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor, layer_past: PastKeyValue | None = None):
        attn_out, present = self.attn(self.ln_1(x), layer_past)
        x = x + attn_out
        x = x + self.mlp(self.ln_2(x))
        return x, present


class GPT(nn.Module):
    """decoder-only 因果 GPT，支持 KV Cache 生成。"""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.config = config
        self.transformer = nn.ModuleDict(
            {
                "wte": nn.Embedding(config.vocab_size, config.n_embd),
                "wpe": nn.Embedding(config.block_size, config.n_embd),
                "h": nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
                "ln_f": nn.LayerNorm(config.n_embd),
            }
        )
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        # 权重绑定：embedding 与输出头共享
        self.transformer.wte.weight = self.lm_head.weight

    def forward(self, idx: torch.Tensor, past_key_values: tuple | None = None):
        """
        Args:
            idx: token ids (B, T)。decode 阶段 T=1。
            past_key_values: 各层缓存的 (K, V) 元组，长度 = n_layer。
                用不可变 ``tuple`` 而非 ``list``，避免调用方误改缓存，更安全。
        """
        B, T = idx.size()
        assert T <= self.config.block_size, "input exceeds block_size"

        tok_emb = self.transformer.wte(idx)
        pos = torch.arange(0, T, device=idx.device)

        if past_key_values is not None:
            cache_len = past_key_values[0][0].size(2)
            pos = pos + cache_len

        pos_emb = self.transformer.wpe(pos)
        x = tok_emb + pos_emb

        presents: list[PastKeyValue] = []
        for i, block in enumerate(self.transformer.h):
            layer_past = past_key_values[i] if past_key_values is not None else None
            x, present = block(x, layer_past)
            presents.append(present)

        x = self.transformer.ln_f(x)
        logits = self.lm_head(x)
        # 返回 tuple，避免外部误改缓存
        return logits, tuple(presents)

    @torch.no_grad()
    def generate(
        self,
        idx: torch.Tensor,
        max_new_tokens: int = 50,
        use_kv_cache: bool = True,
        temperature: float = 1.0,
        top_k: int | None = None,
        sample: bool = True,
    ) -> torch.Tensor:
        """
        自回归生成。

        - ``use_kv_cache=True``：prefill 后每步只喂最后一个 token，解码 O(1)/步。
        - ``use_kv_cache=False``：每步重算整个上下文，解码 O(T)/步。

        Returns:
            生成的 token (B, max_new_tokens)。
        """
        self.eval()
        idx = idx.clone()
        past: tuple | None = None
        generated: list[torch.Tensor] = []

        for _ in range(max_new_tokens):
            if use_kv_cache:
                input_ids = idx[:, -1:] if past is not None else idx
                logits, past = self.forward(input_ids, past)
            else:
                if idx.size(1) >= self.config.block_size:
                    idx = idx[:, -self.config.block_size :]
                logits, _ = self.forward(idx)

            logits = logits[:, -1, :] / temperature
            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = float("-inf")

            if sample:
                probs = F.softmax(logits, dim=-1)
                next_tok = torch.multinomial(probs, num_samples=1)
            else:
                next_tok = logits.argmax(dim=-1, keepdim=True)

            idx = torch.cat([idx, next_tok], dim=1)
            generated.append(next_tok)

        return torch.cat(generated, dim=1)

    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())
