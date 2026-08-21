"""
generate.py — 独立文本生成脚本

加载 `checkpoints/` 下训练好的 checkpoint 与词表，做纯推理生成，无需重新训练。
这是"从研究到产品"的入口：训练一次、随时生成。

用法
----
.. code-block:: bash

    python generate.py --checkpoint checkpoints/best_char_gpt.pth \
        --prompt "清华" --length 300

    # 可选：贪心（无随机）、温度、top-k
    python generate.py --checkpoint checkpoints/best_char_gpt.pth \
        --prompt "如果" --length 200 --temperature 0.9 --top-k 50
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from data.dataset import decode  # noqa: E402
from models.gpt import GPT, GPTConfig  # noqa: E402

DEFAULT_CHECKPOINT = HERE / "checkpoints" / "best_char_gpt.pth"
DEFAULT_VOCAB = HERE / "checkpoints" / "vocab_char.json"


def load_vocab(vocab_path: str | Path):
    """加载词表（char -> idx）与反向映射。"""
    with open(vocab_path, encoding="utf-8") as f:
        char_to_idx = json.load(f)
    idx_to_char = {int(i): c for c, i in char_to_idx.items()}
    return char_to_idx, idx_to_char


def load_model(checkpoint: str | Path, vocab_size: int, device: torch.device) -> GPT:
    """从 checkpoint 加载 GPT。

    优先读取 checkpoint 中保存的模型配置（``{"model", "config"}``，由 train.py 写入）；
    若为旧版纯 state_dict 格式，则从权重名自动恢复结构。
    """
    raw = torch.load(checkpoint, map_location=device)

    if isinstance(raw, dict) and "config" in raw and "model" in raw:
        cfg = GPTConfig(**raw["config"])
        state = raw["model"]
        # 以训练时词表为准
        cfg.vocab_size = cfg.vocab_size
        model = GPT(cfg)
        model.load_state_dict(state)
    else:
        # 旧格式：纯 state_dict
        state = raw
        inferred_vocab = state["lm_head.weight"].shape[0]
        n_embd = state["lm_head.weight"].shape[1]
        n_layer = (
            max(int(k.split(".")[2]) for k in state if k.startswith("transformer.h.")) + 1
        )
        block_size = state["transformer.wpe.weight"].shape[0]
        cfg = GPTConfig(
            vocab_size=inferred_vocab,
            n_embd=n_embd,
            n_layer=n_layer,
            block_size=block_size,
        )
        model = GPT(cfg)
        model.load_state_dict(state)

    model.to(device)
    model.eval()
    return model


def main() -> None:
    p = argparse.ArgumentParser(description="用训练好的字符级 GPT 生成中文")
    p.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    p.add_argument("--vocab", type=str, default=str(DEFAULT_VOCAB))
    p.add_argument("--prompt", type=str, default="清华")
    p.add_argument("--length", type=int, default=300)
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--top-k", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--no-kv", action="store_true", help="关闭 KV Cache（更慢但可对照）")
    args = p.parse_args()

    if args.seed is not None:
        torch.manual_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    char_to_idx, idx_to_char = load_vocab(args.vocab)
    model = load_model(args.checkpoint, len(char_to_idx), device)
    print(f"模型参数量: {model.num_params() / 1e6:.2f}M")

    start = [char_to_idx.get(c, 0) for c in args.prompt]
    x = torch.tensor([start], dtype=torch.long, device=device)
    with torch.no_grad():
        out = model.generate(
            x,
            max_new_tokens=args.length,
            use_kv_cache=not args.no_kv,
            sample=True,
            temperature=args.temperature,
            top_k=args.top_k,
        )

    result = args.prompt + decode(out[0], idx_to_char)
    print("\n" + "=" * 60)
    print("生成结果:")
    print("=" * 60)
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    main()
