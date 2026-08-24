#!/usr/bin/env python3
"""
硬件校准：从实测 (frequency, power) 拟合 `P ≈ α * f^β` 的 `ALPHA / BETA` 系数。

- 默认用示例数据演示（勿用于生产）；
- 用 `--csv` 读取 `collect_power.py` 采集的真实曲线（列含 `core_clock_mhz`、`power_w`）即可拟合真实系数。

用法：
    python scripts/calibrate.py                                   # 示例演示
    python scripts/calibrate.py --csv power_curve.csv             # 用真实采集数据校准
"""

from __future__ import annotations

import argparse
import csv


def fit_power_model(freqs_mhz: list[float], powers_w: list[float]) -> tuple[float, float]:
    """拟合 power = alpha * freq**beta（对数空间线性回归）。"""
    import numpy as np

    log_f = np.log(np.asarray(freqs_mhz, dtype=float))
    log_p = np.log(np.asarray(powers_w, dtype=float))
    # log P = log alpha + beta * log f
    beta, log_alpha = np.polyfit(log_f, log_p, 1)
    alpha = np.exp(log_alpha)
    return float(alpha), float(beta)


def load_csv_points(path: str) -> tuple[list[float], list[float]]:
    """读取 collect_power 的 CSV 中 (core_clock_mhz, power_w) 两列。"""
    freqs: list[float] = []
    powers: list[float] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            f_mhz = (row.get("core_clock_mhz") or "").strip()
            p_w = (row.get("power_w") or "").strip()
            if f_mhz and p_w:
                freqs.append(float(f_mhz))
                powers.append(float(p_w))
    return freqs, powers


def main() -> int:
    p = argparse.ArgumentParser(description="拟合 P≈α·f^β 的 ALPHA/BETA 校准系数")
    p.add_argument("--csv", help="从 collect_power 的 CSV（含 core_clock_mhz, power_w）读取真实数据")
    args = p.parse_args()

    if args.csv:
        freqs, powers = load_csv_points(args.csv)
        if len(freqs) < 2:
            print("⚠️ 有效数据点不足 2 个，请采集更多样本后再校准。")
            return 1
        src = args.csv
    else:
        # 示例：不同频率下的实测功耗（替换为真实测量）
        freqs = [300, 600, 900, 1200, 1500, 1800, 2100]
        powers = [35, 60, 95, 140, 195, 260, 335]
        src = "示例数据"

    alpha, beta = fit_power_model(freqs, powers)
    print(f"校准结果（来源 {src}）：alpha = {alpha:.4f}, beta = {beta:.4f}")
    print(f"P ≈ {alpha:.4f} * f^{beta:.3f}  (可写回 dvfs_controller.py 的 ALPHA/BETA)")
    print("提示：请用真实 GPU 测量数据校准，勿用示例值上生产。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
