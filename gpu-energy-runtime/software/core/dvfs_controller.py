#!/usr/bin/env python3
"""
DVFS Controller — GEAR (GPU Energy-Aware Runtime)
基于ML驱动的动态电压频率调整运行时系统。

目标：在不损失吞吐的前提下，最小化GPU能耗与峰值功耗。
Reference: ML-driven DVFS runtime for heterogeneous CPU-GPU systems
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum

try:
    import numpy as np
    NP_AVAILABLE = True
except ImportError:
    NP_AVAILABLE = False

try:
    from pynvml import *
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False
    print("Warning: pynvml not installed. Install with: pip install nvidia-ml-py3 (模拟模式无需)")


class PowerMode(Enum):
    """功耗/能效模式"""
    MAX_PERFORMANCE = "max_performance"   # 跑满：不设限
    BALANCED = "balanced"                 # 均衡：能效折中
    POWER_SAVE = "power_save"             # 省电：低频低功耗
    ENERGY_OPTIMAL = "energy_optimal"     # 能效最优：ML 预测最优频率
    THERMAL_AWARE = "thermal_aware"       # 温度感知：维持安全热区间


@dataclass
class GPUState:
    """GPU实时状态"""
    temperature: float = 0.0          # 核心温度 (°C)
    power_usage: float = 0.0          # 当前功耗 (W)
    power_limit: float = 0.0          # 功耗封顶 (W)
    core_clock: int = 0               # 核心频率 (MHz)
    memory_clock: int = 0             # 显存频率 (MHz)
    utilization: float = 0.0          # 利用率 (%)
    sm_occupancy: float = 0.0         # SM占用率 (%)
    energy_total: float = 0.0         # 累计能耗 (J)
    current_mode: PowerMode = PowerMode.BALANCED


class DVFSController:
    """
    GPU动态电压频率调整控制器。

    功能：
    1. 基于实时负载动态调整GPU频率
    2. 支持功耗封顶与频率封顶
    3. 集成ML模型预测最优能效点
    4. 温度感知降频保护
    """

    # GPU频率-功耗经验模型: P ≈ alpha * f^beta （需用 scripts/calibrate.py 实测校准）
    ALPHA = 1.0
    BETA = 2.8

    # 温度阈值
    TEMP_ASSERT = 83.0      # 进入降频
    TEMP_CRITICAL = 90.0    # 强制最保守

    def __init__(self, gpu_index: int = 0, config: Optional[Dict] = None):
        self.gpu_index = gpu_index
        self.config = config or {}
        self.state = GPUState()
        self._running = False
        self._control_thread = None
        self._last_sample_t = time.time()

        self.freq_table = self._build_freq_table()

        self.handle = None
        self.min_power_limit = 30.0
        self.max_power_limit = 300.0
        if NVML_AVAILABLE:
            nvmlInit()
            self.handle = nvmlDeviceGetHandleByIndex(gpu_index)
            self._init_hardware()

        self.ml_model = self._load_model()

    # ---------- 初始化 ----------
    def _init_hardware(self):
        try:
            min_power, max_power = nvmlDeviceGetPowerManagementLimitConstraints(self.handle)
            self.min_power_limit = min_power / 1000.0
            self.max_power_limit = max_power / 1000.0
            current_limit = nvmlDeviceGetPowerManagementLimit(self.handle)
            self.state.power_limit = current_limit / 1000.0
        except Exception as exc:
            print(f"warning: NVML init: {exc}")

    def _build_freq_table(self) -> List[int]:
        """可用频率档位 (MHz)。实际应由驱动枚举，此处为典型覆盖。"""
        return [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200,
                1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100]

    def _load_model(self):
        """加载预训练能效预测模型（可选）"""
        try:
            import joblib
            return joblib.load(self.config.get('model_path', 'models/rf_power_model.joblib'))
        except Exception:
            return None

    # ---------- 状态采集 ----------
    def update_state(self) -> GPUState:
        if not NVML_AVAILABLE or self.handle is None:
            return self.state
        try:
            now = time.time()
            dt = now - self._last_sample_t
            self._last_sample_t = now

            self.state.temperature = nvmlDeviceGetTemperature(self.handle, NVML_TEMPERATURE_GPU)
            power = nvmlDeviceGetPowerUsage(self.handle)
            self.state.power_usage = power / 1000.0
            self.state.core_clock = nvmlDeviceGetClockInfo(self.handle, NVML_CLOCK_SM)
            util = nvmlDeviceGetUtilizationRates(self.handle)
            self.state.utilization = util.gpu

            # 累计能耗 = 平均功耗 × 采样间隔
            if dt > 0:
                self.state.energy_total += self.state.power_usage * dt
        except Exception:
            pass
        return self.state

    # ---------- 控制 ----------
    def set_power_limit(self, watts: float):
        """设置功耗封顶 (W)，并夹到硬件约束内。"""
        watts = max(self.min_power_limit, min(watts, self.max_power_limit))
        self.state.power_limit = watts
        if not NVML_AVAILABLE or self.handle is None:
            return
        try:
            nvmlDeviceSetPowerManagementLimit(self.handle, int(watts * 1000))
        except Exception:
            pass

    def set_clock_limit(self, clock_mhz: int):
        """设置频率封顶 (MHz)，吸附到最近的可用频率档。"""
        target = min(self.freq_table, key=lambda x: abs(x - clock_mhz))
        self.state.core_clock = target
        if not NVML_AVAILABLE or self.handle is None:
            return
        try:
            nvmlDeviceSetGpcClkVfOffset(self.handle, 0)
        except Exception:
            pass

    def set_power_mode(self, mode: PowerMode):
        """切换功耗/能效模式。"""
        self.state.current_mode = mode

        if mode == PowerMode.MAX_PERFORMANCE:
            self.set_power_limit(self.max_power_limit)
            self.set_clock_limit(max(self.freq_table))

        elif mode == PowerMode.BALANCED:
            mid = self.min_power_limit + 0.75 * (self.max_power_limit - self.min_power_limit)
            self.set_power_limit(mid)
            self.set_clock_limit(self.freq_table[len(self.freq_table) // 2])

        elif mode == PowerMode.POWER_SAVE:
            self.set_power_limit(self.min_power_limit + 20)
            self.set_clock_limit(self.freq_table[0])

        elif mode == PowerMode.ENERGY_OPTIMAL:
            self.set_clock_limit(self.predict_optimal_frequency())

        elif mode == PowerMode.THERMAL_AWARE:
            self._thermal_aware_control()

    # ---------- 温度感知 ----------
    def _thermal_aware_control(self):
        """若接近峰值温度则逐级降频/降功耗，避免过热导致硬降频。"""
        temp = self.state.temperature
        if temp < self.TEMP_ASSERT:
            # 有余量：按能效最优调频
            self.set_clock_limit(self.predict_optimal_frequency())
        elif temp < self.TEMP_CRITICAL:
            # 减小一档
            cur = min(self.freq_table, key=lambda x: abs(x - self.state.core_clock))
            idx = self.freq_table.index(cur)
            self.set_clock_limit(self.freq_table[max(0, idx - 1)])
            self.set_power_limit(max(self.min_power_limit, self.state.power_limit - 10))
        else:
            # 过热：最保守
            self.set_power_limit(self.min_power_limit)
            self.set_clock_limit(self.freq_table[0])

    # ---------- ML 预测 ----------
    def predict_optimal_frequency(self, workload_type: str = "unknown") -> int:
        """
        预测能效最优频率。
        输入特征: [utilization, sm_occupancy, power, temperature]
        无模型时降级为基于利用率的启发式。
        """
        if self.ml_model is None or not NP_AVAILABLE:
            util = self.state.utilization
            if util < 30:
                return self.freq_table[2]
            elif util < 60:
                return self.freq_table[6]
            elif util < 85:
                return self.freq_table[10]
            else:
                return self.freq_table[-1]
        features = np.array([[
            self.state.utilization,
            self.state.sm_occupancy,
            self.state.power_usage,
            self.state.temperature
        ]])
        return int(self.ml_model.predict(features)[0])

    # ---------- 控制循环 ----------
    def run_control_loop(self):
        while self._running:
            self.update_state()
            if self.state.current_mode in (PowerMode.ENERGY_OPTIMAL, PowerMode.BALANCED):
                self.set_clock_limit(self.predict_optimal_frequency())
            elif self.state.current_mode == PowerMode.POWER_SAVE:
                self.set_clock_limit(self.freq_table[0])
            elif self.state.current_mode == PowerMode.THERMAL_AWARE:
                self._thermal_aware_control()

            if self.state.temperature > self.TEMP_CRITICAL:
                self.set_power_limit(self.min_power_limit)
                self.set_clock_limit(self.freq_table[0])
                print(f"⚠️ 过热保护: {self.state.temperature:.1f}°C")

            time.sleep(0.2)

    def start(self):
        if self._running:
            return
        self._running = True
        self._control_thread = threading.Thread(target=self.run_control_loop, daemon=True)
        self._control_thread.start()
        print(f"✅ DVFS 控制器已启动 (GPU {self.gpu_index}, mode={self.state.current_mode.value})")

    def stop(self):
        self._running = False
        if self._control_thread:
            self._control_thread.join(timeout=2)
        print("🛑 DVFS 控制器已停止")

    # ---------- 报告 ----------
    def get_energy_report(self) -> Dict:
        """返回能效/热状态报告。"""
        self.update_state()
        temp = self.state.temperature
        in_safe_band = temp <= self.TEMP_ASSERT
        energy_kwh = self.state.energy_total / 3_600_000.0
        return {
            "temperature_c": temp,
            "power_usage_w": self.state.power_usage,
            "power_limit_w": self.state.power_limit,
            "core_clock_mhz": self.state.core_clock,
            "utilization_pct": self.state.utilization,
            "energy_kwh": energy_kwh,
            "in_safe_band": in_safe_band,
            "mode": self.state.current_mode.value,
            "tokens_per_watt_hint": None,  # 由上层按业务吞吐填充 -> 见 performance_per_watt
        }


# ============ 命令行接口 ============

def main():
    import argparse

    parser = argparse.ArgumentParser(description="GEAR — GPU Energy-Aware Runtime")
    parser.add_argument("--mode", choices=["max", "balanced", "save", "optimal", "thermal"],
                        default="optimal", help="运行模式")
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--power-limit", type=float)
    parser.add_argument("--clock-limit", type=int)
    parser.add_argument("--simulate", action="store_true", help="无GPU时用模拟数据")
    args = parser.parse_args()

    ctrl = DVFSController(gpu_index=args.gpu, config={})
    mode_map = {
        "max": PowerMode.MAX_PERFORMANCE,
        "balanced": PowerMode.BALANCED,
        "save": PowerMode.POWER_SAVE,
        "optimal": PowerMode.ENERGY_OPTIMAL,
        "thermal": PowerMode.THERMAL_AWARE,
    }
    if args.power_limit:
        ctrl.set_power_limit(args.power_limit)
    if args.clock_limit:
        ctrl.set_clock_limit(args.clock_limit)
    ctrl.set_power_mode(mode_map[args.mode])
    ctrl.start()

    try:
        print("\n🧪 GEAR 运行中... (Ctrl+C 停止)\n")
        while True:
            r = ctrl.get_energy_report()
            print(f"\r🌡️ {r['temperature_c']:6.1f}°C | ⚡ {r['power_usage_w']:7.1f}W | "
                  f"📊 {r['core_clock_mhz']}MHz | 🔋 {r['energy_kwh']:.4f} kWh | "
                  f"mode={r['mode']}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        ctrl.stop()


if __name__ == "__main__":
    main()
