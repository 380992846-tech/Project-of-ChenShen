#!/usr/bin/env python3
"""
GEAR 基准：跑 GPU 负载，记录温度/功耗/频率曲线，并计算**性能功耗比（tokens/s/W）**。

复用 `scripts/collect_power.py` 的采样式；接入真实业务吞吐后即可得到核心能效指标：
    perf-per-watt = 吞吐(tokens/s) / 平均功耗(W)

用法：
    # 无 GPU 演示（确定性模拟曲线）
    python scripts/run_benchmark.py --simulate --duration 20 --throughput 1000
    # 真机基准（DVFS ENERGY_OPTIMAL），记录曲线 + perf-per-watt
    python scripts/run_benchmark.py --duration 60 --throughput 2500 --mode optimal --out bench.csv
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collect_power import NVML_AVAILABLE, run_collector  # noqa: E402
from core.dvfs_controller import PowerMode  # noqa: E402

_MODE_MAP = {
    "max": PowerMode.MAX_PERFORMANCE,
    "balanced": PowerMode.BALANCED,
    "save": PowerMode.POWER_SAVE,
    "optimal": PowerMode.ENERGY_OPTIMAL,
    "thermal": PowerMode.THERMAL_AWARE,
}


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    p = argparse.ArgumentParser(description="GEAR 基准：记录功率曲线 + 性能功耗比")
    p.add_argument("--duration", type=float, default=30.0, help="采集时长 (s)")
    p.add_argument("--interval", type=float, default=1.0, help="采样间隔 (s)")
    p.add_argument("--throughput", type=float, help="平均吞吐 (tokens/s)，算 perf-per-watt")
    p.add_argument("--out", default="benchmark_curve.csv", help="CSV 输出路径")
    p.add_argument("--mode", choices=list(_MODE_MAP), default="optimal", help="DVFS 模式（真机生效）")
    p.add_argument("--simulate", action="store_true", help="无 GPU 时用确定性模拟")
    args = p.parse_args()

    simulate = args.simulate or not NVML_AVAILABLE
    if simulate:
        print("⚠️ 无 NVML/模拟：用确定性曲线演示；真机请 pip install nvidia-ml-py3")

    print(f"跑基准 {args.duration:.0f}s（间隔 {args.interval:.1f}s，吞吐={args.throughput}，mode={args.mode}）...")
    summary = run_collector(args.duration, args.interval, args.out, simulate,
                            throughput=args.throughput, mode=_MODE_MAP[args.mode])

    print("=" * 56)
    print(f"样本数           : {summary['count']}")
    print(f"平均功耗         : {summary['avg_power_w']} W")
    print(f"峰值功耗         : {summary['peak_power_w']} W")
    print(f"峰值温度         : {summary['peak_temp_c']} °C")
    print(f"累计能耗         : {summary['energy_kwh']} kWh")
    if summary["perf_per_watt"] is not None:
        print(f"性能功耗比       : {summary['perf_per_watt']} tok/s/W")
    else:
        print("性能功耗比       : 加 --throughput（真实吞吐）后才有意义")
    print(f"CSV 已写        : {args.out}")


if __name__ == "__main__":
    main()
