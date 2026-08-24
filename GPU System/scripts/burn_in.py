#!/usr/bin/env python3
"""GPU 烧机测试（Burn-in）：在**无法硬件锁频**的容器环境里，用纯浮点矩阵乘榨干 GPU。

目标
----
1. 让 GPU 在高负载下自动睿频到稳定点，采集满载稳态的 (核心频率, 功耗) 观测；
2. 通过切换矩阵规模（算力档）采集多个点，观察"算力 ↑ → 功耗 ↑"的相关性——
   容器内频率不可控时，**矩阵规模**是更可靠的变量。

诚实边界（为何不拟合 ``P≈α·f^β``）
----------------------------------
- 容器默认无 ``nvidia-smi -lgc`` 锁频权限，GPU Boost 在高负载下通常自动顶到最高频，
  各档位**频率差异极小**，频率不是可控变量，因此**无法可靠拟合频率-功耗模型**；
- 脚本会检测频率跨度并**如实提示**（而非产出无意义的假参数）；
- 若要获得可信的 ``ALPHA / BETA``，需在**物理裸机 / 可锁频环境**运行
  ``scripts/frequency_sweep.py`` 做逐档锁频扫描。

适用
----
- 受限容器（云 GPU 等）下验证负载与功耗 / TDP 的相关性，以及实验设计是否严谨；
- 配合 ``scripts/plot_burnin.py`` 绘制"算力 → 功耗"散点图。

用法
----
    python scripts/burn_in.py --levels 8192 12288 16384 --stable 4 --out burn_in.csv
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
    # 用 FP16 打满张量核（fp32 只有 fp16 的约 1/15 算力，无法榨干 A800）
    a = torch.rand(shape, shape, device="cuda", dtype=torch.float16)
    b = torch.rand(shape, shape, device="cuda", dtype=torch.float16)
    for _ in range(10):            # 预热，避免启动开销
        _ = a @ b
    torch.cuda.synchronize()
    end = time.time() + seconds
    while time.time() < end:
        for _ in range(4):         # 一次循环内连续多次，让 GPU 持续满载
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
        print("   本环境由于锁频限制，改为采集「算力规模(矩阵大小) 与 功耗」的关系。")
        print("   该数据可用于验证负载与热设计功耗(TDP)的物理相关性，是受限环境下的有效观测。")
        print("   如需可信 ALPHA/BETA，请在物理裸机/可锁频环境跑 frequency_sweep.py。")
    print("=" * 46)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
