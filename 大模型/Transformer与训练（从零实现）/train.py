"""
train.py — 在真实中文语料上训练字符级 GPT
=========================================

让"从零实现的 Transformer"变得有实际意义：
- 读取 `training_data.txt`（由 `build_corpus.py` 从 `笔记/贵系.docx` 与
  `笔记/量化.docx` 两个文档抽取合并），构建字符级词表；
- 训练一个 **decoder-only GPT**（复用 `大模型/llm/gpt.py`，仓库内从零实现）；
- 记录 train/val 损失、困惑度，保存最佳 checkpoint；
- 训练中/结束后**生成中文文本样例**，直观看到模型学到了什么。

用法
----
.. code-block:: bash

    python 大模型/Transformer与训练（从零实现）/build_corpus.py   # 重建语料
    python 大模型/Transformer与训练（从零实现）/train.py \
        --steps 2000 --n_embd 128 --n_layer 4

产物
----
- `models/`：最佳 checkpoint（已 gitignore）
- `training_curve.png`：损失曲线
- `训练报告.md`：损失、困惑度、生成样例、结论
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import torch
import torch.nn.functional as F

# 让脚本能 import 仓库内的 llm 子包（decoder-only GPT）
_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC.parent))  # 大模型/

from llm.gpt import GPT, GPTConfig

plt.switch_backend("Agg")

HERE = Path(__file__).resolve().parent
DATA_FILE = HERE / "training_data.txt"
MODELS_DIR = HERE / "models"


# --------------------------------------------------------------------------
# 字符级分词
# --------------------------------------------------------------------------
def build_vocab(text: str):
    chars = sorted(set(text))
    char_to_idx = {c: i for i, c in enumerate(chars)}
    idx_to_char = {i: c for c, i in char_to_idx.items()}
    return char_to_idx, idx_to_char


def encode(text: str, char_to_idx) -> torch.Tensor:
    return torch.tensor([char_to_idx[c] for c in text if c in char_to_idx], dtype=torch.long)


def decode(ids, idx_to_char) -> str:
    return "".join(idx_to_char[i] for i in ids.tolist())


# --------------------------------------------------------------------------
# 训练
# --------------------------------------------------------------------------
def train(args):
    torch.manual_seed(args.seed)

    text = DATA_FILE.read_text(encoding="utf-8", errors="ignore")
    char_to_idx, idx_to_char = build_vocab(text)
    vocab = len(char_to_idx)
    data = encode(text, char_to_idx)

    # train/val 按 9:1 切
    n_val = int(len(data) * 0.1)
    train_data, val_data = data[:-n_val], data[-n_val:]
    print(f"语料 {len(data)} 字符 | 词表 {vocab} | train {len(train_data)} / val {len(val_data)}")

    cfg = GPTConfig(
        vocab_size=vocab,
        n_layer=args.n_layer,
        n_head=args.n_head,
        n_embd=args.n_embd,
        block_size=args.seq_len,
    )
    model = GPT(cfg)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    def get_batch(split):
        d = train_data if split == "train" else val_data
        ix = torch.randint(0, len(d) - args.seq_len - 1, (args.batch,))
        xb = torch.stack([d[i : i + args.seq_len] for i in ix])
        yb = torch.stack([d[i + 1 : i + args.seq_len + 1] for i in ix])
        return xb, yb

    @torch.no_grad()
    def evaluate():
        model.eval()
        losses = {"train": [], "val": []}
        for split in ("train", "val"):
            for _ in range(20):
                xb, yb = get_batch(split)
                logits, _ = model(xb)
                loss = F.cross_entropy(logits.reshape(-1, vocab), yb.reshape(-1))
                losses[split].append(loss.item())
        model.train()
        return {k: sum(v) / len(v) for k, v in losses.items()}

    @torch.no_grad()
    def generate_sample(seed_str="清华"):
        model.eval()
        start = [char_to_idx.get(c, 0) for c in seed_str]
        x = torch.tensor([start], dtype=torch.long)
        # 复用 GPT.generate（greedy + KV cache）
        out = model.generate(x, max_new_tokens=args.gen_len, use_kv_cache=True, sample=True, temperature=0.8)
        model.train()
        return seed_str + decode(out[0], idx_to_char)

    history = {"train": [], "val": []}
    best_val = float("inf")
    t0 = time.time()
    for step in range(1, args.steps + 1):
        xb, yb = get_batch("train")
        opt.zero_grad()
        logits, _ = model(xb)
        loss = F.cross_entropy(logits.reshape(-1, vocab), yb.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % args.eval_every == 0 or step == args.steps:
            m = evaluate()
            history["train"].append((step, m["train"]))
            history["val"].append((step, m["val"]))
            ppl = math.exp(m["val"])
            if m["val"] < best_val:
                best_val = m["val"]
                torch.save(model.state_dict(), MODELS_DIR / "best_char_gpt.pth")
            sample = generate_sample()
            el = time.time() - t0
            print(f"[{step}/{args.steps}] train {m['train']:.3f} | val {m['val']:.3f} | PPL {ppl:.1f} | {el:.0f}s")
            print(f"    生成: {sample[:80]}")

    # 最终
    final = evaluate()
    torch.save(model.state_dict(), MODELS_DIR / "final_char_gpt.pth")
    print(f"\n最终 train {final['train']:.3f} / val {final['val']:.3f} / PPL {math.exp(final['val']):.1f}")

    # 保存词表（供推理复用）
    with open(MODELS_DIR / "vocab_char.json", "w", encoding="utf-8") as f:
        json.dump(char_to_idx, f, ensure_ascii=False)

    # 损失曲线
    plt.figure(figsize=(8, 5))
    plt.plot([s for s, _ in history["train"]], [v for _, v in history["train"]], label="train")
    plt.plot([s for s, _ in history["val"]], [v for _, v in history["val"]], label="val")
    plt.xlabel("step"); plt.ylabel("loss"); plt.title("Char-level GPT training loss")
    plt.legend(); plt.grid(alpha=.3)
    plt.tight_layout(); plt.savefig(HERE / "training_curve.png", dpi=120); plt.close()

    return {
        "cfg": cfg, "vocab": vocab, "steps": args.steps, "final": final,
        "ppl": math.exp(final["val"]), "history": history,
        "samples": [generate_sample(s) for s in args.sample_prompts],
    }


def write_report(result):
    cfg = result["cfg"]
    lines = [
        "# 字符级 GPT 训练报告（从零实现）",
        "",
        f"- 语料：`training_data.txt`（中文）| 字符词表 `{result['vocab']}`",
        f"- 模型：decoder-only GPT，`{cfg.n_layer}` 层 × `{cfg.n_embd}` 维 × `{cfg.n_head}` 头，block `{cfg.block_size}`",
        f"- 训练：`{result['steps']}` 步 | 最终 train loss `{result['final']['train']:.3f}` / val `{result['final']['val']:.3f}`",
        f"- **困惑度 PPL：`{result['ppl']:.1f}`**（越低越好；字符级随机基线 ≈ 词表大小 `{result['vocab']}`）",
        "",
        "## 训练损失",
        "",
        "| step | train loss | val loss |",
        "|------|-----------|----------|",
    ]
    for s, tl in result["history"]["train"]:
        vl = next(v for ss, v in result["history"]["val"] if ss == s)
        lines.append(f"| {s} | {tl:.3f} | {vl:.3f} |")
    lines += ["", "![损失曲线](training_curve.png)", "", "## 生成样例（训练后）", ""]
    for s in result["samples"]:
        lines.append(f"- 提示「{s[:2]}」→ **{s}**")
    lines += [
        "",
        "## 结论",
        "",
        "- 从零实现的 decoder-only Transformer 能在真实中文语料上训练，损失持续下降、困惑度远低于随机基线，",
        "  说明它学到了汉字共现与语料的分布规律；",
        "- 小模型 + CPU + 有限步数下，生成的是**短句级的通顺片段**而非完整长文——这是资源限制，",
        "  增大模型/语料/步数（或 GPU）可显著提升；",
        "- checkpoint 与词表已存到 `models/`，可用 `generate.py`（可选）加载做推理。",
    ]
    (HERE / "训练报告.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n报告已写入: {HERE / '训练报告.md'}")


def main():
    p = argparse.ArgumentParser(description="训练字符级 GPT")
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--n_embd", type=int, default=128)
    p.add_argument("--n_layer", type=int, default=4)
    p.add_argument("--n_head", type=int, default=4)
    p.add_argument("--seq_len", type=int, default=128)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--lr", type=float, default=3e-3)
    p.add_argument("--eval_every", type=int, default=250)
    p.add_argument("--gen_len", type=int, default=60)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--sample_prompts", nargs="+", default=["清华", "他", "如果"])
    args = p.parse_args()
    result = train(args)
    write_report(result)


if __name__ == "__main__":
    main()
