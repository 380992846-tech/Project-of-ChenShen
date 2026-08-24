#!/usr/bin/env python3
"""GPU 频率-功耗扫描，拟合 DVFS 模型 `P ≈ α · f^β`。

对每个目标核心频率：`nvidia-smi -lgc` 锁定 → 跑 GPU 密集负载(torch) → 读平均功耗 → `-rgc` 复位。
最终用 (频率, 功耗) 点拟合出可写回 `dvfs_controller.py` 的 ALPHA / BETA。

前提：
  - 需 **root 权限** + NVIDIA 驱动支持锁频（`nvidia-smi -lgc` 能成功）；
  - 建议先停掉其它占用 GPU 的进程（如 vLLM server），避免干扰。

用法：python scripts/frequency_sweep.py --load-secs 5 --stable-secs 3 --out sweep.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "software"))

import pynvml  # noqa: E402

DEFAULT_FREQS = [300, 600, 900, 1200, 1500, 1800, 2100]


def gpu_power() -> float:
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    return pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0


def lock(mhz: int, span: int = 0) -> bool:
    r = subprocess.run(
        ["nvidia-smi", "-i", "0", "-lgc", f"{max(0, mhz - span)},{mhz + span}"],
        capture_output=True, text=True,
    )
    return r.returncode == 0


def unlock() -> None:
    subprocess.run(["nvidia-smi", "-i", "0", "-rgc"], capture_output=True)


def burn(seconds: float) -> None:
    import torch

    torch.cuda.init()
    a = torch.rand(4096, 4096, device="cuda")
    b = torch.rand(4096, 4096, device="cuda")
    end = time.time() + seconds
    while time.time() < end:
        _ = a @ b
    torch.cuda.synchronize()
    del a, b
    torch.cuda.empty_cache()


def main() -> int:
    ap = argparse.ArgumentParser(description="GPU 频率-功耗扫描 + 拟合 ALPHA/BETA")
    ap.add_argument("--load-secs", type=float, default=5.0, help="每档负载时长(s)")
    ap.add_argument("--stable-secs", type=float, default=3.0, help="每档读功耗时长(s)")
    ap.add_argument("--freqs", type=int, nargs="+", default=DEFAULT_FREQS, help="要扫描的频率档(MHz)")
    ap.add_argument("--out", default="sweep.csv", help="输出 CSV")
    args = ap.parse_args()

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    # NVML 未提供最小时钟 API（nvmlDeviceGetMinClockInfo 不存在），
    # 此处只取最大核心频率作为上限约束；最小频率以经验参考（A100/A800 ≈ 210 MHz）兜底。
    max_clock = int(pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_SM))
    min_clock = 210
    print(f"硬件最大核心频率: {max_clock} MHz  (上限约束；最小频率 NVML 未暴露，参考 {min_clock} MHz)")

    freqs = [f for f in args.freqs if min_clock <= f <= max_clock]
    if not freqs:
        print("⚠️ 所有请求档位都超出硬件频率范围，未执行扫描。")
        unlock()
        return 1
    if len(freqs) != len(args.freqs):
        print(f"   (已跳过 {len(args.freqs) - len(freqs)} 个超出范围的档位)")

    points: list[tuple[int, float]] = []
    for f in freqs:
        if not lock(f):
            print(f"⚠️ 锁频 {f}MHz 失败：需要 root 权限 + 驱动支持（nvidia-smi -lgc）。")
            unlock()
            return 1
        try:
            burn(args.load_secs)          # 负载先把 GPU 跑热/稳定
            time.sleep(0.5)
            samples = [gpu_power() for _ in range(int(args.stable_secs * 2))]
            avg = sum(samples) / len(samples)
            print(f"{f} MHz -> {avg:.1f} W")
            points.append((f, avg))
        finally:
            unlock()

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["core_clock_mhz", "power_w"])
        w.writerows(points)

    freqs = [p[0] for p in points]
    powers = [p[1] for p in points]
    import numpy as np

    beta, log_alpha = np.polyfit(np.log(freqs), np.log(powers), 1)
    alpha = float(np.exp(log_alpha))
    print("\n" + "=" * 46)
    print(f"拟合结果（{len(points)} 个频率档）：")
    print(f"  ALPHA = {alpha:.4f}")
    print(f"  BETA  = {beta:.4f}")
    print(f"  P ≈ {alpha:.4f} * f^{beta:.4f}")
    print("可写回 dvfs_controller.py 的 ALPHA / BETA")
    print("=" * 46)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
