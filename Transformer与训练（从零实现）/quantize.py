"""
quantize.py — 模型量化（INT8 动态量化）

把 `complete_ai_toolkit.py` 的量化功能拆出为独立模块，适配 decoder-only GPT。
对 Linear / Embedding 做 PyTorch 动态 INT8 量化，并对比 FP32 / INT8 推理耗时。

用法
----
.. code-block:: bash

    python quantize.py --checkpoint checkpoints/best_char_gpt.pth
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from generate import load_model, load_vocab  # noqa: E402


def measure_speed(model: nn.Module, test_input: torch.Tensor, runs: int = 50) -> float:
    """测量平均前向耗时（ms）。"""
    model.eval()
    times = []
    with torch.no_grad():
        for _ in range(runs):
            t0 = time.time()
            model(test_input)
            times.append((time.time() - t0) * 1000)
    return float(sum(times) / len(times))


def quantize(checkpoint: str, vocab: str) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    char_to_idx, _ = load_vocab(vocab)
    model = load_model(checkpoint, len(char_to_idx), device)

    # 校准/测试输入
    vocab_size = model.config.vocab_size
    test_input = torch.randint(0, vocab_size, (1, 64), device=device)

    print(f"\n=== 模型量化 ===")
    print(f"模型参数量: {model.num_params() / 1e6:.2f}M")
    fp32_time = measure_speed(model, test_input)
    print(f"FP32 推理时间: {fp32_time:.2f} ms")

    # 动态 INT8 量化（CPU 上对 Linear/Embedding）
    int8_model = torch.quantization.quantize_dynamic(
        model, {nn.Linear, nn.Embedding}, dtype=torch.qint8
    )
    int8_time = measure_speed(int8_model.to("cpu"), test_input.to("cpu"))
    print(f"INT8 推理时间: {int8_time:.2f} ms (CPU)")
    print(f"加速比: {fp32_time / max(int8_time, 1e-6):.2f}x")

    torch.save(int8_model.state_dict(), HERE / "checkpoints" / "model_int8.pth")
    print("量化模型已保存到 checkpoints/model_int8.pth")


def main() -> None:
    p = argparse.ArgumentParser(description="字符级 GPT 量化")
    p.add_argument("--checkpoint", type=str, default=str(HERE / "checkpoints" / "best_char_gpt.pth"))
    p.add_argument("--vocab", type=str, default=str(HERE / "checkpoints" / "vocab_char.json"))
    args = p.parse_args()
    quantize(args.checkpoint, args.vocab)


if __name__ == "__main__":
    main()
