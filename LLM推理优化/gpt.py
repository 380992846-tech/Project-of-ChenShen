"""
gpt.py
======

一个简洁的 decoder-only GPT（因果 Transformer），核心目标是演示**推理优化**：

- **KV Cache**：解码时缓存每一层的 K/V，避免每步重算整个上下文。
- **prefill / decode 分离**：首步一次性处理完整 prompt（prefill），
  后续每步只输入最后一个 token（decode）。

与 ``complete_ai_toolkit.py`` 的 encoder-only CharTransformer 不同，
本模块是**自回归（causal）**结构，KV Cache 只对这类模型成立。

用法示例
--------
.. code-block:: python

    from llm.gpt import GPT, GPTConfig

    cfg = GPTConfig(vocab_size=256, n_layer=4, n_head=4, n_embd=128)
    model = GPT(cfg)
    prompt = torch.randint(0, 256, (1, 32))

    out_kv = model.generate(prompt, max_new_tokens=50, use_kv_cache=True, sample=False)
    out_plain = model.generate(prompt, max_new_tokens=50, use_kv_cache=False, sample=False)
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

        # 因果下三角掩码（prefill / 全序列前向时使用），shape (1,1,block_size,block_size)
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

        # 因果掩码：
        # - prefill / 全序列前向（cache_len==0）：下三角掩码；
        # - decode 且 T==1：当前唯一 query 能看到全部缓存键，无需掩码（省开销）；
        # - decode 且 T>1（如投机解码一次性验证多个草稿 token）：新 token 之间
        #   需因果掩码——query i 可见缓存键 0..cache_len-1 与新增键 0..i。
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

    def forward_padded(
        self,
        x: torch.Tensor,
        k_pad: torch.Tensor,
        v_pad: torch.Tensor,
        cache_len: torch.Tensor,
    ):
        """
        continuous batching 用的**变长 KV** 前向。

        Args:
            x: (B, T, n_embd)。continuous batching 的 decode 步通常 T=1。
            k_pad, v_pad: 已按最大长度填充的缓存 (B, n_head, max_len, head_dim)。
            cache_len: (B,) 每个请求**本轮之前**已缓存的有效 token 数。

        Returns:
            (y, (new_k_pad, new_v_pad))：输出，以及把本轮新 token 写入后的填充缓存。
        """
        B, T, C = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)

        head, hd = self.n_head, self.head_dim
        q = q.view(B, T, head, hd).transpose(1, 2)
        k = k.view(B, T, head, hd).transpose(1, 2)
        v = v.view(B, T, head, hd).transpose(1, 2)

        max_len = k_pad.size(2)
        new_k = k_pad.clone()
        new_v = v_pad.clone()
        # 把本轮新 token 的 K/V 写入各请求的有效区段
        for r in range(B):
            start = int(cache_len[r].item())
            new_k[r, :, start : start + T, :] = k[r]
            new_v[r, :, start : start + T, :] = v[r]

        att = (q @ new_k.transpose(-2, -1)) * (1.0 / math.sqrt(hd))  # (B,H,T,max_len)
        # per-row 掩码：有效键下标 < cache_len[r] + T，其余 -inf
        pos = torch.arange(max_len, device=x.device).view(1, 1, 1, max_len)
        valid_until = cache_len.view(B, 1, 1, 1) + T
        att = att.masked_fill(pos >= valid_until, float("-inf"))

        att = F.softmax(att, dim=-1)
        att = self.dropout(att)
        y = att @ new_v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.c_proj(y)
        return y, (new_k, new_v)


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

    def forward_padded(
        self,
        x: torch.Tensor,
        k_pad: torch.Tensor,
        v_pad: torch.Tensor,
        cache_len: torch.Tensor,
    ):
        """continuous batching 的 Block 前向（变长 KV + per-row 掩码）。"""
        attn_out, (nk, nv) = self.attn.forward_padded(self.ln_1(x), k_pad, v_pad, cache_len)
        x = x + attn_out
        x = x + self.mlp(self.ln_2(x))
        return x, (nk, nv)


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

    def forward(self, idx: torch.Tensor, past_key_values: list | None = None):
        """
        Args:
            idx: token ids (B, T)。decode 阶段 T=1。
            past_key_values: 各层缓存的 (K, V) 列表，长度 = n_layer。
        """
        B, T = idx.size()
        assert T <= self.config.block_size, "input exceeds block_size"

        tok_emb = self.transformer.wte(idx)
        pos = torch.arange(0, T, device=idx.device)

        # decode 阶段新 token 的位置 = 缓存长度（接在已有序列之后）
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
        return logits, presents

    @torch.no_grad()
    def forward_continuous(
        self,
        idx: torch.Tensor,
        past_pads: list[PastKeyValue] | None,
        cache_lens: torch.Tensor,
        buffer_len: int | None = None,
    ):
        """
        continuous batching 前向：batch 内各请求可拥有**不同长度的 KV 缓存**。

        Args:
            idx: (B, T) token。decode 步通常 T=1。
            past_pads: 每层 (k_pad, v_pad)，shape (B, n_head, buffer_len, head_dim)。
            cache_lens: (B,) 每请求本轮之前的有效缓存 token 数。
            buffer_len: 首次调用时的 KV 缓冲区长度（默认 block_size）。
        Returns:
            (logits, past_pads)：logits (B, T, vocab) 与更新后的填充缓存。
        """
        B, T = idx.size()
        tok_emb = self.transformer.wte(idx)
        # 每请求位置 = cache_len[r] + t
        pos = cache_lens.unsqueeze(1) + torch.arange(T, device=idx.device).view(1, T)
        pos_emb = self.transformer.wpe(pos)
        x = tok_emb + pos_emb

        new_pads: list[PastKeyValue] = []
        for i, block in enumerate(self.transformer.h):
            k_pad, v_pad = past_pads[i] if past_pads is not None else (None, None)
            if k_pad is None:
                # 首次调用：按 buffer_len 初始化填充缓存
                max_len = buffer_len or self.config.block_size
                n_head = block.attn.n_head
                head_dim = block.attn.head_dim
                k_pad = torch.zeros(B, n_head, max_len, head_dim, device=idx.device)
                v_pad = torch.zeros_like(k_pad)
            x, (nk, nv) = block.forward_padded(x, k_pad, v_pad, cache_lens)
            new_pads.append((nk, nv))

        x = self.transformer.ln_f(x)
        logits = self.lm_head(x)
        return logits, new_pads

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

        - ``use_kv_cache=True``：prefill 后每步只喂最后一个 token，解码 O(1)/步（不随序列增长）。
        - ``use_kv_cache=False``：每步重算整个上下文，解码 O(T)/步。

        Args:
            idx: 初始 prompt (B, T)。
            sample: True 用 ``multinomial`` 采样；False 用贪心 ``argmax``（用于确定性测试）。
        Returns:
            生成的 token (B, max_new_tokens)。
        """
        self.eval()
        idx = idx.clone()
        past: list | None = None
        generated: list[torch.Tensor] = []

        for _ in range(max_new_tokens):
            if use_kv_cache:
                # 首步 prefill 处理整段 prompt，之后只喂最后一个 token
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
