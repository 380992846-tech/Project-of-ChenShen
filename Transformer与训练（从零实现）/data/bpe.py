"""data/bpe.py — 极简 BPE（Byte Pair Encoding）分词器

字符级 GPT 的天然升级：BPE 把常见子词合并成 token，能显著压缩序列长度、
提高建模效率（中文尤其明显）。本实现是教学级简化版（不做 byte-level 回退），
聚焦 BPE 核心：迭代合并最高频相邻对。

用法
----
.. code-block:: bash

    # 训练 BPE 词表（vocab_size 个 merge 合并出 vocab_size+初始字符 token 数）
    python -m data.bpe train --corpus training_data.txt --vocab-size 2000 --out checkpoints/bpe_vocab.json

    # 查看分词效果
    python -m data.bpe encode --vocab checkpoints/bpe_vocab.json --text "清华大学"

API::

    from data.bpe import BPETokenizer
    bpe = BPETokenizer.train(corpus, vocab_size=2000)
    ids = bpe.encode("清华大学")
    text = bpe.decode(ids)
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

# 初始字符 token：常见的可打印 ASCII + 中文常用范围用 Unicode 单字符兜底
_SPECIAL = ["<unk>", "<pad>"]
# 空白统一替换为这个保留字符（BPE 标准做法，如 SentencePiece 的 ▁），
# 这样空格能在 token 流里保留、可还原，避免 decode 丢空白。
_WS_PLACEHOLDER = "▁"
_PRE_TOKENIZE = re.compile(r"\s+")  # 仅用于识别空白字符


def _normalize(text: str) -> str:
    """把每个空白字符替换为占位符（逐个，不合并），供 BPE 处理。"""
    return "".join(_WS_PLACEHOLDER if ch.isspace() else ch for ch in text)


def _denormalize(text: str) -> str:
    """把占位符还原为空格。"""
    return text.replace(_WS_PLACEHOLDER, " ")


class BPETokenizer:
    """教学级 BPE 分词器。"""

    def __init__(self, vocab: dict):
        # vocab: {token_str: id}
        self.vocab = vocab
        self.id_to_token = {i: t for t, i in vocab.items()}

    # ------------------------------------------------------------ 训练
    @classmethod
    def train(cls, corpus: str, vocab_size: int = 2000) -> "BPETokenizer":
        # 归一化空白为占位符，保证空格可还原；▁ 作为普通 token 参与 BPE
        corpus = _normalize(corpus)
        # 初始词汇：特殊 token + 语料里出现过的所有单字符（含 ▁）
        chars = sorted(set(corpus))
        vocab = {t: i for i, t in enumerate(_SPECIAL + chars)}
        # 若目标词表大小 <= 初始字符数，无法合并，直接返回字符级
        if len(vocab) >= vocab_size:
            tok = cls(vocab)
            tok.merges = []
            return tok

        # 经典加速版 BPE（Kevin Gimpel）：整段归一化文本作为一个长 token 序列，
        # 相邻对跨位置统计，增量更新，避免全量重扫语料。
        seqs: list[list[str]] = [list(corpus)]
        pair_counts: Counter = Counter()
        pair_locations: dict[tuple, list[tuple[int, int]]] = defaultdict(list)
        for wi, s in enumerate(seqs):
            for i in range(len(s) - 1):
                p = (s[i], s[i + 1])
                pair_counts[p] += 1
                pair_locations[p].append((wi, i))

        merges: list[tuple[str, str]] = []
        while len(vocab) < vocab_size and pair_counts:
            (a, b), _ = pair_counts.most_common(1)[0]
            merged = a + b
            vocab[merged] = len(vocab)
            merges.append((a, b))

            # 收集所有含 (a,b) 的词索引（去重）
            affected = {wi for (wi, i) in pair_locations.pop((a, b), [])}

            # 逐个受影响词：先删除其全部旧 pair 统计，再线性合并，再重建统计
            for wi in affected:
                s = seqs[wi]
                # 删除该词的所有旧 pair 统计
                for i in range(len(s) - 1):
                    p = (s[i], s[i + 1])
                    pair_counts[p] -= 1
                    if pair_counts[p] <= 0:
                        del pair_counts[p]
                # 线性合并 (a,b) -> merged
                new_s: list[str] = []
                i = 0
                while i < len(s):
                    if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                        new_s.append(merged)
                        i += 2
                    else:
                        new_s.append(s[i])
                        i += 1
                seqs[wi] = new_s
                # 重建该词的新 pair 统计
                for i in range(len(new_s) - 1):
                    p = (new_s[i], new_s[i + 1])
                    pair_counts[p] += 1
                    pair_locations[p].append((wi, i))

        tok = cls(vocab)
        tok.merges = merges
        return tok

    # ------------------------------------------------------------ 编解码
    def encode(self, text: str) -> list[int]:
        """归一化后对整个文本应用 merge，返回 id 列表。"""
        norm = _normalize(text)  # 空白 -> 占位符，保证空格可还原
        toks = list(norm)
        for a, b in self.merges:
            merged = a + b
            new_toks = []
            i = 0
            while i < len(toks):
                if i + 1 < len(toks) and toks[i] == a and toks[i + 1] == b:
                    new_toks.append(merged)
                    i += 2
                else:
                    new_toks.append(toks[i])
                    i += 1
            toks = new_toks
        return [self.vocab.get(t, self.vocab.get("<unk>", 0)) for t in toks]

    def decode(self, ids: list[int]) -> str:
        return _denormalize(
            "".join(self.id_to_token.get(i, "<unk>") for i in ids)
        )

    # ------------------------------------------------------------ 持久化
    def save(self, path: str | Path) -> None:
        payload = {"vocab": self.vocab, "merges": getattr(self, "merges", [])}
        Path(path).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "BPETokenizer":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        tok = cls(payload["vocab"])
        tok.merges = payload.get("merges", [])
        return tok


def _cli_train(corpus, vocab_size, out):
    text = Path(corpus).read_text(encoding="utf-8", errors="ignore")
    tok = BPETokenizer.train(text, vocab_size=vocab_size)
    tok.save(out)
    print(f"BPE 词表已保存: {out}（{len(tok.vocab)} tokens）")
    sample = tok.encode("清华大学计算机系")
    print("示例: '清华大学计算机系' ->", sample)
    print("  decode ->", tok.decode(sample))


def _cli_encode(vocab, text):
    tok = BPETokenizer.load(vocab)
    ids = tok.encode(text)
    print("ids:", ids)
    print("text:", tok.decode(ids))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="BPE 分词器工具")
    sub = p.add_subparsers(dest="cmd", required=True)
    pt = sub.add_parser("train")
    pt.add_argument("--corpus", default="training_data.txt")
    pt.add_argument("--vocab-size", type=int, default=2000)
    pt.add_argument("--out", default="checkpoints/bpe_vocab.json")
    pe = sub.add_parser("encode")
    pe.add_argument("--vocab", default="checkpoints/bpe_vocab.json")
    pe.add_argument("--text", default="清华大学")
    args = p.parse_args()

    if args.cmd == "train":
        _cli_train(args.corpus, args.vocab_size, args.out)
    else:
        _cli_encode(args.vocab, args.text)
