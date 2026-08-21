"""
rag.py — 检索增强生成（RAG）

把 `complete_ai_toolkit.py` 的 ``SimpleRAG`` 拆出为独立模块，适配本项目
decoder-only GPT（`models/gpt.py`）。支持两种检索：
- 语义检索（需 ``sentence-transformers``，未安装时自动降级）；
- 关键词检索（纯 Python，零依赖）。

用法
----
.. code-block:: bash

    python rag.py --checkpoint checkpoints/best_char_gpt.pth \
        --query "什么是清华？" --docs "notes.txt"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

# Windows 控制台默认 GBK，强制 UTF-8 输出避免 print 中文时崩溃
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from data.dataset import decode  # noqa: E402
from generate import load_model, load_vocab  # noqa: E402
from models.gpt import GPT  # noqa: E402


class SimpleRAG:
    """检索增强生成系统。"""

    def __init__(
        self,
        generator: GPT,
        char_to_idx: dict,
        idx_to_char: dict,
        device: str = "cpu",
    ):
        self.generator = generator
        self.char_to_idx = char_to_idx
        self.idx_to_char = idx_to_char
        self.device = device
        self.documents: list[str] = []
        self.embeddings: np.ndarray | list[str] | None = None

        # 尝试加载语义编码器，否则用关键词检索
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            print("✓ 已加载 Embedding 模型（语义检索）")
        except ImportError:
            print("⚠ 未安装 sentence-transformers，使用关键词检索")
            self.encoder = None

    def build_index(self, documents: list[str]) -> None:
        self.documents = documents
        if self.encoder:
            self.embeddings = self.encoder.encode(documents)
        else:
            self.embeddings = [doc.lower() for doc in documents]

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        if self.encoder:
            from sklearn.metrics.pairwise import cosine_similarity
            query_vec = self.encoder.encode([query])
            similarities = cosine_similarity(query_vec, self.embeddings)[0]
            top_indices = similarities.argsort()[-top_k:][::-1]
        else:
            query_words = set(query.lower().split())
            scores = [
                len(query_words & set(doc.lower().split()))
                for doc in self.embeddings
            ]
            top_indices = np.argsort(scores)[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]

    def generate_answer(self, query: str, length: int = 200) -> str:
        context = self.retrieve(query)
        prompt = f"根据以下资料回答问题：\n{chr(10).join(context)}\n\n问题：{query}\n答案："
        start = [self.char_to_idx.get(c, 0) for c in prompt]
        import torch
        x = torch.tensor([start], dtype=torch.long, device=self.device)
        with torch.no_grad():
            out = self.generator.generate(x, max_new_tokens=length, sample=True, temperature=0.7)
        return prompt + decode(out[0], self.idx_to_char)


def main() -> None:
    p = argparse.ArgumentParser(description="RAG 问答（字符级 GPT）")
    p.add_argument("--checkpoint", type=str, default=str(HERE / "checkpoints" / "best_char_gpt.pth"))
    p.add_argument("--vocab", type=str, default=str(HERE / "checkpoints" / "vocab_char.json"))
    p.add_argument("--query", type=str, default="什么是清华？")
    p.add_argument("--docs", type=str, nargs="+", default=[])
    p.add_argument("--top-k", type=int, default=3)
    args = p.parse_args()

    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    char_to_idx, idx_to_char = load_vocab(args.vocab)
    model = load_model(args.checkpoint, len(char_to_idx), device)

    rag = SimpleRAG(model, char_to_idx, idx_to_char, device=device)
    if args.docs:
        docs = []
        for d in args.docs:
            pth = Path(d)
            if pth.exists():
                docs.append(pth.read_text(encoding="utf-8", errors="ignore"))
        rag.build_index(docs)

    answer = rag.generate_answer(args.query)
    print("\n" + "=" * 60)
    print("RAG 答案:")
    print("=" * 60)
    print(answer[-300:])
    print("=" * 60)


if __name__ == "__main__":
    main()
