"""test_dataset.py — 数据集与分词工具测试。"""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.dataset import CharDataset, build_vocab, decode, encode  # noqa: E402


def test_build_vocab_roundtrip():
    text = "你好，世界"
    char_to_idx, idx_to_char = build_vocab(text)
    ids = encode(text, char_to_idx)
    assert decode(ids, idx_to_char) == text


def test_dataset_shapes():
    text = "这是一个用于测试的中文语料。" * 20
    ds = CharDataset(text, seq_len=16)
    assert len(ds) > 0
    x, y = ds[0]
    assert x.shape == (16,)
    assert y.shape == (16,)
    assert x.dtype == torch.long


def test_dataset_next_token():
    """y 是 x 的右移一位（next-token 预测）。"""
    text = "abcde" * 30
    ds = CharDataset(text, seq_len=8)
    x, y = ds[0]
    assert (y[:-1] == x[1:]).all()


def test_vocab_size():
    text = "ab" * 50
    ds = CharDataset(text, seq_len=8)
    assert ds.vocab_size == 2
