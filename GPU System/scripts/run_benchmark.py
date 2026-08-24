#!/usr/bin/env python3
"""
基准测试：跑 GPU 负载，记录温度/功耗/频率曲线，用于校准与能效评估。
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "software"))
from core.dvfs_controller import DVFSController, PowerMode


def main():
    ctrl = DVFSController(gpu_index=0, config={})
    ctrl.set_power_mode(PowerMode.ENERGY_OPTIMAL)

    print("跑基准 30s：记录温度/功耗/频率曲线（用于能效评估）")
    start = time.time()
    while time.time() - start < 30:
        st = ctrl.get_energy_report()
        print(f"\r🌡️ {st['temperature_c']:.1f}°C | ⚡ {st['power_usage_w']:.1f}W | "
              f"📊 {st['core_clock_mhz']}MHz | 🔋 {st['energy_kwh']:.4f} kWh",
              end="")
        time.sleep(1)
    print("\n✅ 基准完成。")


if __name__ == "__main__":
    main()
