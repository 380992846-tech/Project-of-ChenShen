"""data 包：语料构建与数据集。"""
from .dataset import CharDataset, build_vocab, decode, encode

__all__ = ["CharDataset", "build_vocab", "decode", "encode"]
