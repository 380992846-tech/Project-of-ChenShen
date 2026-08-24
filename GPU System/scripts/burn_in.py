#!/usr/bin/env python3
"""GPU 烧机测试：纯浮点矩阵乘榨干 GPU，采集稳定 (核心频率, 功耗)。

用于在**无法硬件锁频**的容器环境（如 AutoDL）里，用高负载让 GPU 睿频到稳定点，
记录真实频率-功耗观测；也可跑多个"算力档"（不同矩阵规模）尝试拉开频率。

诚实边界：
  - 容器无法 `nvidia-smi -lgc` 锁频时，GPU Boost 在高负载下通常**自动顶到最高频**，
    不同档位频率差异可能很小，此时**无法可靠拟合 `P≈α·f^β`**（脚本会检测并提示）；
  - 要得到可信的 α/β，仍需**物理裸机/可锁频环境**跑 `frequency_sweep.py`。

用法：
    python scripts/burn_in.py --levels 2048 4096 6144 --stable 3 --out burn_in.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "software"))

import pynvml  # noqa: E402


def burn(seconds: float, shape: int) -> None:
    import torch

    torch.cuda.init()
    a = torch.rand(shape, shape, device="cuda")
    b = torch.rand(shape, shape, device="cuda")
    end = time.time() + seconds
    while time.time() < end:
        _ = a @ b
    torch.cuda.synchronize()
    del a, b
    torch.cuda.empty_cache()


def read_state() -> tuple[int, float]:
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
    return int(clock), power


def run_level(shape: int, warmup: float, stable: float) -> tuple[int, float]:
    burn(warmup, shape)          # 预热，让负载稳定
    time.sleep(0.5)
    clocks: list[int] = []
    powers: list[float] = []
    for _ in range(int(stable * 2)):
        c, p = read_state()
        clocks.append(c)
        powers.append(p)
        time.sleep(0.5)
    return round(sum(clocks) / len(clocks)), sum(powers) / len(powers)


def main() -> int:
    ap = argparse.ArgumentParser(description="GPU 烧机测试：采集稳定(频率,功耗)")
    ap.add_argument("--levels", type=int, nargs="+", default=[2048, 4096, 6144], help="矩阵规模档")
    ap.add_argument("--warmup", type=float, default=3.0, help="每档预热(s)")
    ap.add_argument("--stable", type=float, default=3.0, help="每档采功耗(s)")
    ap.add_argument("--out", default="burn_in.csv", help="输出 CSV")
    args = ap.parse_args()

    pynvml.nvmlInit()
    points: list[tuple[int, int, float]] = []
    for shape in args.levels:
        clock, power = run_level(shape, args.warmup, args.stable)
        print(f"shape={shape}  ->  {clock} MHz / {power:.1f} W")
        points.append((shape, clock, power))

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["matrix_size", "core_clock_mhz", "power_w"])
        w.writerows(points)

    # 检测频率是否有区分度，决定能否拟合
    clocks = [p[1] for p in points]
    powers = [p[2] for p in points]
    span = max(clocks) - min(clocks)
    print("\n" + "=" * 46)
    print(f"频率跨度: {span} MHz  ({min(clocks)} ~ {max(clocks)})")
    if span >= 200:
        import numpy as np

        beta, log_alpha = np.polyfit(np.log(clocks), np.log(powers), 1)
        alpha = float(np.exp(log_alpha))
        print(f"拟合: ALPHA={alpha:.4f}  BETA={beta:.4f}")
        print(f"  P ≈ {alpha:.4f} * f^{beta:.4f}   (可回填 dvfs_controller)")
        if beta <= 0:
            print("  ⚠️ BETA<=0 异常：数据不可靠，勿回填。")
    else:
        print("⚠️ 各档频率几乎恒定（GPU 自动睿频到满频），无法拟合「频率→功耗」关系。")
        print("   需要物理裸机/可锁频环境跑 frequency_sweep.py 才能得到可信 ALPHA/BETA。")
        print("   本脚本产出的是「满载稳态(频率,功耗)」观测，可作参考。")
    print("=" * 46)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
