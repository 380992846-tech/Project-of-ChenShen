"""
train_utils.py
==============

字符级 GPT 的训练与评测工具（供量化对比、投机解码等实验复用）。
"""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F

from gpt import GPT, GPTConfig


def build_tokenizer(text: str):
    chars = sorted(set(text))
    char_to_idx = {c: i for i, c in enumerate(chars)}
    idx_to_char = {i: c for i, c in enumerate(chars)}
    return char_to_idx, idx_to_char


def encode(text: str, char_to_idx) -> list[int]:
    return [char_to_idx[c] for c in text if c in char_to_idx]


def train_char_gpt(
    train_text: str,
    *,
    n_layer: int = 3,
    n_embd: int = 64,
    n_head: int = 4,
    steps: int = 400,
    batch_size: int = 8,
    seq_len: int = 128,
    seed: int = 0,
) -> tuple[GPT, dict, dict]:
    torch.manual_seed(seed)
    char_to_idx, idx_to_char = build_tokenizer(train_text)
    vocab = len(char_to_idx)
    cfg = GPTConfig(
        vocab_size=vocab,
        n_layer=n_layer,
        n_head=n_head,
        n_embd=n_embd,
        block_size=seq_len,
        dropout=0.0,
    )
    model = GPT(cfg)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)

    data = torch.tensor(encode(train_text, char_to_idx), dtype=torch.long)
    n = data.numel()

    for step in range(steps):
        ix = torch.randint(0, n - seq_len - 1, (batch_size,))
        xb = torch.stack([data[i : i + seq_len] for i in ix])
        yb = torch.stack([data[i + 1 : i + seq_len + 1] for i in ix])
        opt.zero_grad()
        logits, _ = model(xb)
        loss = F.cross_entropy(logits.reshape(-1, vocab), yb.reshape(-1))
        loss.backward()
        opt.step()

    return model, char_to_idx, idx_to_char


@torch.no_grad()
def evaluate_ppl(model: GPT, data: torch.Tensor, seq_len: int = 128) -> float:
    model.eval()
    vocab = model.config.vocab_size
    nll, n = 0.0, 0
    for i in range(0, data.numel() - seq_len, seq_len):
        xb = data[i : i + seq_len].unsqueeze(0)
        yb = data[i + 1 : i + seq_len + 1].unsqueeze(0)
        logits, _ = model(xb)
        loss = F.cross_entropy(logits.reshape(-1, vocab), yb.reshape(-1))
        nll += loss.item() * (seq_len - 1)
        n += seq_len - 1
    return math.exp(nll / n)
