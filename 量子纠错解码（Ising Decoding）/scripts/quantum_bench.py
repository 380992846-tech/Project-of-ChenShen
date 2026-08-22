"""
quantum_bench.py — 量子纠错解码基准测试（第一阶段）

对比 NVIDIA Ising Decoding（颜色代码 AI 预解码器）与行业标准 pyMatching。

目标指标：
- 速度：Ising 相对 pyMatching 的吞吐提升（目标 ≥ 2.5×）
- 精度：逻辑错误率降低倍数（目标 ≥ 3×）

参考 `LLM推理优化/benchmark.py` 的结构：确定性、可复现、结果落盘。

用法（规划中，依赖官方 ising-decoding / stim / pymatching 安装后使用）：
    python scripts/quantum_bench.py --decoder ising --distance 3 --shots 1000
    python scripts/quantum_bench.py --decoder pymatching --distance 3 --shots 1000
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def measure_ising(distance: int, shots: int, model_size: str):
    """用 Ising 预解码器解码，测量吞吐与逻辑错误率。"""
    # 占位：需接入官方 ising-decoding 或加载 HF 预训练模型
    raise NotImplementedError(
        "第一阶段：接入 NVIDIA/ising-decoding 或 "
        "hf:nvidia/Ising-Decoder-ColorCode-1-Fast"
    )


def measure_pymatching(distance: int, shots: int):
    """用 pyMatching 匹配解码器解码，作为基线。"""
    # 占位：需用 stim 生成颜色代码电路 + pymatching 解码
    raise NotImplementedError("需安装 stim + pymatching，生成颜色代码 benchmark 电路")


def main() -> None:
    p = argparse.ArgumentParser(description="量子纠错解码基准：Ising vs pyMatching")
    p.add_argument("--decoder", choices=["ising", "pymatching"], default="ising")
    p.add_argument("--distance", type=int, default=3, help="码距")
    p.add_argument("--shots", type=int, default=1000, help="解码轮数")
    p.add_argument("--model-size", choices=["fast", "accurate"],
                   default="fast", help="0.9M(fast) / 1.8M(accurate)")
    p.add_argument("--save", action="store_true", help="保存结果")
    args = p.parse_args()

    if args.decoder == "ising":
        perf, err = measure_ising(args.distance, args.shots, args.model_size)
    else:
        perf, err = measure_pymatching(args.distance, args.shots)

    print(f"decoder={args.decoder} d={args.distance} shots={args.shots}")
    print(f"  吞吐 (decode/s): {perf}")
    print(f"  逻辑错误率: {err}")

    if args.save:
        RESULTS.mkdir(exist_ok=True)
        out = RESULTS / f"bench_{args.decoder}_d{args.distance}.json"
        out.write_text(
            json.dumps(vars(args) | {"throughput": perf, "logical_error_rate": err},
                       indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[save] {out}")


if __name__ == "__main__":
    main()
