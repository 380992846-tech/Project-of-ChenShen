#!/usr/bin/env python3
"""
GEAR — GPU Energy-Aware Runtime · CLI 遥测仪表盘
实时展示：温度 / 功耗 / 频率 / 利用率 / 累计能耗 / 性能功耗比 / 热状态建议。

无真实 GPU 时以模拟数据运行（--simulate），有 NVIDIA GPU + pynvml 时自动用真实硬件。
"""

import os
import sys
import time
import argparse
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 强制 UTF-8 输出（避免 Windows GBK 打印 emoji/中文报错）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from core.dvfs_controller import DVFSController, PowerMode, NVML_AVAILABLE
from core.thermal_manager import ThermalManager


BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║   ⚙  G E A R  ·  GPU Energy-Aware Runtime  v1.0             ║
║   ⚡ 能耗感知 DVFS  ·  功耗封顶  ·  温度保护                ║
╚══════════════════════════════════════════════════════════════╝
"""


def boot_sequence(simulate: bool) -> None:
    print(BANNER)
    print("> 检测硬件……")
    if simulate or not NVML_AVAILABLE:
        print("✅ 模拟模式：无真实 GPU / NVML，使用模拟传感器（仅演示）")
    else:
        print("✅ 已连接 NVIDIA GPU（NVML 真实硬件）")
        print("✅ 功耗封顶与频率约束可用")

    print("\n> 初始化控制栈……")
    print("✅ DVFS 控制器")
    print("✅ 热管理 / 温度保护")
    print("✅ ML 能效预测（可选，models/rf_power_model.joblib）")
    print("\n> 启动模式：ENERGY_OPTIMAL（能效最优）\n")


class SimEngine:
    """模拟 GPU 负载/温度/功耗（无 GPU 演示用）。"""

    def __init__(self):
        self.temp = 40.0
        self.power = 120.0
        self.clock = 1200
        self.util = 60.0
        self.tokens = 0
        self.t = 0.0

    def tick(self, dt: float = 1.0):
        self.t += dt
        if self.temp < 76.0:
            self.temp += dt * 3.5
        else:
            self.temp += 0.15 if (int(self.t) % 5) else -0.1
        self.temp = max(35.0, min(86.0, self.temp))
        self.power = 140.0 + self.temp * 1.2
        self.clock = 1500 + int(self.temp * 4.5)
        self.clock = min(2100, self.clock)
        self.util = min(99.0, 52 + self.temp * 0.55)
        # 模拟吞吐（tokens/s），随频率/利用率；真机请替换为业务吞吐计数
        self.tps = self.clock * self.util / 1000.0


def bar(value, lo, hi, width=18):
    if hi <= lo:
        return "░" * width
    frac = max(0.0, min(1.0, (value - lo) / (hi - lo)))
    return "█" * int(frac * width) + "░" * (width - int(frac * width))


def run_dashboard(args):
    sim = args.simulate or not NVML_AVAILABLE
    boot_sequence(sim)

    thermal = ThermalManager()
    sim_engine = SimEngine() if sim else None
    ctrl = DVFSController(gpu_index=args.gpu, config={})

    mode = {
        "max": PowerMode.MAX_PERFORMANCE,
        "balanced": PowerMode.BALANCED,
        "save": PowerMode.POWER_SAVE,
        "optimal": PowerMode.ENERGY_OPTIMAL,
        "thermal": PowerMode.THERMAL_AWARE,
    }[args.mode]

    if args.power_limit:
        ctrl.set_power_limit(args.power_limit)
    if args.clock_limit:
        ctrl.set_clock_limit(args.clock_limit)
    ctrl.set_power_mode(mode)
    ctrl.start()

    energy_j = 0.0
    start = time.time()
    last = time.time()

    frame = 0
    print("🌡️ 单帧预览\n" if args.once else "🌡️ 遥测监控（Ctrl+C 停止）\n")
    try:
        while True:
            now = time.time()
            dt = now - last
            last = now

            if sim_engine is not None:
                sim_engine.tick(dt)
                temp = sim_engine.temp
                power = sim_engine.power
                clock = sim_engine.clock
                util = sim_engine.util
                tps = sim_engine.tps            # tokens/s（模拟吞吐）
            else:
                r = ctrl.get_energy_report()
                temp = r["temperature_c"]
                power = r["power_usage_w"]
                clock = r["core_clock_mhz"]
                util = r["utilization_pct"]
                tps = util                      # 占位：真机请接入业务吞吐计数

            energy_j += power * dt
            energy_kwh = energy_j / 3_600_000.0
            thermal.update_thermal_state(temp)
            guidance = thermal.thermal_guidance()

            # 性能功耗比 = 瞬时吞吐 / 功耗 (tokens per second per Watt)
            perf_per_w = (tps / power) if power > 0 else 0.0
            elapsed = int(now - start)

            if frame > 0:
                os.system("cls" if os.name == "nt" else "clear")
            print(BANNER)
            print(f"时间: {time.strftime('%H:%M:%S')}  |  运行: {elapsed//60:02d}:{elapsed%60:02d}  |"
                  f"  {'模拟' if sim else '真实硬件'}  |  mode={args.mode}")
            print("┌──────────────────────────────────────────────────────┐")
            print(f"│ GPU 温度   : {temp:6.1f}°C  {bar(temp, 35, 90)}  {guidance['status']:>8}  │")
            print(f"│ GPU 功耗   : {power:7.1f} W  {bar(power, 0, 300)}      │")
            print(f"│ 核心频率   : {clock:5d} MHz {bar(clock, 300, 2100)}      │")
            print(f"│ 利用率     : {util:5.1f} %  {bar(util, 0, 100)}      │")
            print(f"│ 累计能耗   : {energy_kwh:8.4f} kWh                   │")
            print(f"│ 热回收     : {guidance['heat_recovery_w']:6.1f} W                     │")
            print("└──────────────────────────────────────────────────────┘")
            print(f"\n♨️  热状态: {guidance['action']}")
            print(f"⚡ 性能功耗比(perf/W): {perf_per_w:.3f} tok/s/W  (接入真实吞吐后该值才有意义)")
            frame += 1
            if args.once:
                break
            time.sleep(max(0.5, 1.0 - dt))

    except KeyboardInterrupt:
        ctrl.stop()
        print(f"\n🛑 已停止。累计能耗 {energy_kwh:.4f} kWh。")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="GEAR — GPU Energy-Aware Runtime")
    p.add_argument("--mode", choices=["max", "balanced", "save", "optimal", "thermal"], default="optimal")
    p.add_argument("--gpu", type=int, default=0)
    p.add_argument("--power-limit", type=float)
    p.add_argument("--clock-limit", type=int)
    p.add_argument("--simulate", action="store_true", help="无 GPU 时用模拟数据")
    p.add_argument("--once", action="store_true", help="只打印一帧后退出（便于截图/CI）")
    args = p.parse_args()
    run_dashboard(args)
