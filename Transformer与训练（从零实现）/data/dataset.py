"""data/dataset.py — 字符级数据集与分词工具

- ``build_vocab`` / ``encode`` / ``decode``：字符级分词；
- ``CharDataset``：把文本切成 (x, y) 序列对，供训练/验证使用。

用法示例::

    from data.dataset import CharDataset

    ds = CharDataset(text, seq_len=128)
    x, y = ds[0]            # x: (128,), y: (128,)
    print(len(ds), ds.vocab_size)
"""

from __future__ import annotations

import torch
from torch.utils.data import Dataset


def build_vocab(text: str):
    """根据文本构建字符词表。"""
    chars = sorted(set(text))
    char_to_idx = {c: i for i, c in enumerate(chars)}
    idx_to_char = {i: c for c, i in char_to_idx.items()}
    return char_to_idx, idx_to_char


def encode(text: str, char_to_idx) -> torch.Tensor:
    """把字符串编码为 token 向量（跳过不在词表内的字符）。"""
    return torch.tensor([char_to_idx[c] for c in text if c in char_to_idx], dtype=torch.long)


def decode(ids, idx_to_char) -> str:
    """把 token 向量解码为字符串。"""
    return "".join(idx_to_char[i] for i in ids.tolist())


class CharDataset(Dataset):
    """字符级序列数据集，按 seq_len 切分并做 next-token 预测。"""

    def __init__(
        self,
        text: str,
        seq_len: int = 128,
        char_to_idx: dict | None = None,
        idx_to_char: dict | None = None,
    ):
        self.seq_len = seq_len

        if char_to_idx is None:
            char_to_idx, idx_to_char = build_vocab(text)

        self.char_to_idx = char_to_idx
        self.idx_to_char = idx_to_char
        self.vocab_size = len(char_to_idx)

        self.data = torch.tensor(
            [char_to_idx.get(ch, 0) for ch in text], dtype=torch.long
        )

        # 重叠采样：每次前进 seq_len//2，得到相邻序列对 (x, y)
        self.xs: list[torch.Tensor] = []
        self.ys: list[torch.Tensor] = []
        step = max(1, seq_len // 2)
        for i in range(0, len(self.data) - seq_len - 1, step):
            self.xs.append(self.data[i : i + seq_len])
            self.ys.append(self.data[i + 1 : i + seq_len + 1])

    def __len__(self) -> int:
        return len(self.xs)

    def __getitem__(self, idx: int):
        return self.xs[idx], self.ys[idx]
