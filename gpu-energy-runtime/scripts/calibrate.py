#!/usr/bin/env python3
"""
硬件校准：从实测 (фrequency, power) 拟合 P ≈ α * f^β 的 ALPHA/BETA 系数。
默认用示例数据演示；接真实数据时改成从 CSV/nvidia-smi 读取。
"""

import numpy as np


def fit_power_model(freqs_mhz, powers_w):
    """拟合 power = alpha * freq**beta （对数空间线性回归）。"""
    log_f = np.log(np.asarray(freqs_mhz, dtype=float))
    log_p = np.log(np.asarray(powers_w, dtype=float))
    # log P = log alpha + beta * log f
    beta, log_alpha = np.polyfit(log_f, log_p, 1)
    alpha = np.exp(log_alpha)
    return alpha, beta


def main():
    # 示例：不同频率下的实测功耗（替换为真实测量）
    freqs = [300, 600, 900, 1200, 1500, 1800, 2100]
    powers = [35, 60, 95, 140, 195, 260, 335]
    alpha, beta = fit_power_model(freqs, powers)
    print(f"校准结果：alpha = {alpha:.4f}, beta = {beta:.4f}")
    print(f"P ≈ {alpha:.4f} * f^{beta:.3f}  (写回 dvfs_controller.py 的 ALPHA/BETA)")
    print("提示：请用真实 GPU 测量数据校准，勿用示例值上生产。")


if __name__ == "__main__":
    main()
