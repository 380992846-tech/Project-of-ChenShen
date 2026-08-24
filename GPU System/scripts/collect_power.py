#!/usr/bin/env python3
"""
实测功率曲线 + 真实 PUE 落地骨架：周期性采集并记录 GPU 功耗/温度/频率/利用率。

产出：
  - 实测时间序列写入 CSV（时间戳/温度/功耗/频率/利用率/显存利用率/累计能耗）→ 供画功率曲线；
  - 汇总：平均/峰值功耗、峰值温度、累计能耗；
  - 估算 PUE：``PUE = 机房总功率 / IT 总功率``，由 ``--facility-power-w`` 与 ``--it-power-w`` 计算。

用法：
  # 无 GPU 演示（确定性模拟曲线）
  python scripts/collect_power.py --simulate --duration 20

  # 真实硬件采集 60s，并画功率曲线（需 matplotlib）
  python scripts/collect_power.py --duration 60 --chart

  # 带整机/机房口径，估算 PUE（需 --facility-power-w 与 --it-power-w）
  python scripts/collect_power.py --duration 60 --facility-power-w 120000 --it-power-w 40000

诚实边界（不夸大）：
  - GPU 功耗来自 NVML（IT 设备侧）；真实 PUE 需要机房级「总功率/IT 功率」数据，
    本脚本无法自行侦测机房总功率，只能对你提供的两个数做除法，属"按给定口径计算"。
  - 采集频率上限受 nvidia-smi/NVML 轮询与权限限制，请勿据此断言能效结论。
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys
import time
from dataclasses import asdict, dataclass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "software"))

from core.dvfs_controller import NVML_AVAILABLE, DVFSController, PowerMode  # noqa: E402


@dataclass
class PowerSample:
    """一次采样。"""
    t: float            # 时间戳(epoch)
    temperature_c: float
    power_w: float
    core_clock_mhz: int
    util_pct: float
    mem_util_pct: float
    energy_kwh: float


CSV_HEADER = ["t", "temperature_c", "power_w", "core_clock_mhz", "util_pct",
              "mem_util_pct", "energy_kwh"]


class SimulatedGauge:
    """无 GPU 时的确定性模拟负载（演示/CI，曲线随正弦波动）。"""

    def __init__(self):
        self.t0 = time.time()
        self.energy_kwh = 0.0
        self.last_t = time.time()

    def sample(self, now: float) -> PowerSample:
        el = now - self.t0
        dt = max(0.0, now - self.last_t)
        self.last_t = now
        # 负载随正弦波动，模拟周期性工作负载
        util = 55.0 + 40.0 * math.sin(el / 6.0)
        temp = 52.0 + 24.0 * (util / 100.0)
        power = 90.0 + 150.0 * (util / 100.0)
        clock = 800 + int(1200.0 * (util / 100.0))
        clock = min(2100, clock)
        self.energy_kwh += (power * dt) / 3_600_000.0
        return PowerSample(now, round(temp, 1), round(power, 1), clock,
                           round(util, 1), round(55 + 30 * math.sin(el / 4.0), 1),
                           self.energy_kwh)


def write_csv(path: str, samples: list[PowerSample]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        for s in samples:
            w.writerow(asdict(s))


def summarize(samples: list[PowerSample], throughput: float | None = None) -> dict:
    powers = [s.power_w for s in samples]
    temps = [s.temperature_c for s in samples]
    if not samples:
        return {"count": 0, "avg_power_w": 0.0, "peak_power_w": 0.0,
                "peak_temp_c": 0.0, "energy_kwh": 0.0, "duration_s": 0.0,
                "perf_per_watt": None}
    energy = samples[-1].energy_kwh
    avg_power = sum(powers) / len(powers)
    summary = {
        "count": len(samples),
        "avg_power_w": round(avg_power, 1),
        "peak_power_w": round(max(powers), 1),
        "peak_temp_c": round(max(temps), 1),
        "energy_kwh": round(energy, 4),
        "duration_s": round(samples[-1].t - samples[0].t, 1),
    }
    # 性能功耗比 = 吞吐 tokens/s / 平均功耗 W（接入真实吞吐才有意义）
    if throughput is not None and avg_power > 0:
        summary["perf_per_watt"] = round(throughput / avg_power, 3)
    else:
        summary["perf_per_watt"] = None
    return summary


def compute_pue(facility_w: float | None, it_w: float | None) -> float | None:
    """PUE = 机房总功率 / IT 总功率；缺参或 IT<=0 时返回 None。"""
    if facility_w is None or it_w is None or it_w <= 0:
        return None
    return round(facility_w / it_w, 3)


def sample_real(ctrl: DVFSController, now: float) -> PowerSample:
    r = ctrl.get_energy_report()
    return PowerSample(now, r["temperature_c"], r["power_usage_w"], r["core_clock_mhz"],
                       r["utilization_pct"], r.get("memory_utilization_pct", 0.0), r["energy_kwh"])


def run_collector(duration: float, interval: float, out_path: str,
                  simulate: bool, facility_w: float | None = None,
                  it_w: float | None = None, throughput: float | None = None,
                  mode: PowerMode | None = None) -> dict:
    ctrl = None if simulate else DVFSController(gpu_index=0, config={})
    if ctrl is not None and mode is not None:
        ctrl.set_power_mode(mode)
    gauge = SimulatedGauge() if simulate else None
    samples: list[PowerSample] = []
    start = time.time()
    while time.time() - start < duration:
        now = time.time()
        s = gauge.sample(now) if simulate else sample_real(ctrl, now)
        samples.append(s)
        time.sleep(max(0.05, interval))
    if out_path:
        write_csv(out_path, samples)
    summary = summarize(samples, throughput=throughput)
    pue = compute_pue(facility_w, it_w)
    if pue is not None:
        summary["pue_estimate"] = pue
    return summary


def plot_chart(out_path: str, samples: list[PowerSample]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ts = [s.t - samples[0].t for s in samples]
    pw = [s.power_w for s in samples]
    plt.figure(figsize=(10, 5))
    plt.plot(ts, pw, color="#b28aff", lw=2)
    plt.xlabel("time (s)")
    plt.ylabel("GPU power (W)")
    plt.title("GPU Power Curve")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    p = argparse.ArgumentParser(description="实测 GPU 功率曲线采集记录器")
    p.add_argument("--duration", type=float, default=30.0, help="采集时长 (s)")
    p.add_argument("--interval", type=float, default=1.0, help="采样间隔 (s)")
    p.add_argument("--out", default="power_curve.csv", help="CSV 输出路径")
    p.add_argument("--simulate", action="store_true", help="无 GPU 时用确定性模拟数据")
    p.add_argument("--facility-power-w", type=float, help="机房总功率 (W)，用于估算 PUE")
    p.add_argument("--it-power-w", type=float, help="IT 总功率 (W)，用于估算 PUE")
    p.add_argument("--throughput", type=float, help="平均吞吐 (tokens/s)，用于计算 perf-per-watt")
    p.add_argument("--chart", action="store_true", help="生成功率曲线 PNG（需 matplotlib）")
    args = p.parse_args()

    if args.simulate:
        print("✅ 模拟模式：确定性曲线（演示/CI）")
    elif NVML_AVAILABLE:
        print("✅ 真实硬件：NVML 采集")
    else:
        print("⚠️ 未安装/未检测到 NVML，回退模拟；若需真机请 pip install nvidia-ml-py3")
        args.simulate = True

    print(f"采集 {args.duration:.0f}s（间隔 {args.interval:.1f}s）...")
    summary = run_collector(args.duration, args.interval, args.out, args.simulate,
                            args.facility_power_w, args.it_power_w, args.throughput)
    print("=" * 56)
    print(f"样本数           : {summary['count']}")
    print(f"平均功耗         : {summary['avg_power_w']} W")
    print(f"峰值功耗         : {summary['peak_power_w']} W")
    print(f"峰值温度         : {summary['peak_temp_c']} °C")
    print(f"累计能耗         : {summary['energy_kwh']} kWh")
    print(f"采集时长         : {summary['duration_s']} s")
    if summary["perf_per_watt"] is not None:
        print(f"性能功耗比       : {summary['perf_per_watt']} tok/s/W  (吞吐 {args.throughput:.1f} tok/s)")
    else:
        print("性能功耗比       : 接入 --throughput（真实吞吐）后才有意义")
    if "pue_estimate" in summary:
        print(f"PUE(按给定口径)  : {summary['pue_estimate']}")
    print(f"CSV 已写        : {args.out}")

    if args.chart:
        import logging

        logging.getLogger("matplotlib").setLevel(logging.ERROR)
        with open(args.out, newline="", encoding="utf-8") as f:
            rows = [PowerSample(**{k: (float(v) if k != "core_clock_mhz" else int(float(v)))
                                    for k, v in row.items()})
                    for row in csv.DictReader(f)]
        chart_path = os.path.splitext(args.out)[0] + ".png"
        plot_chart(chart_path, rows)
        print(f"曲线图已写        : {chart_path}")


if __name__ == "__main__":
    main()
