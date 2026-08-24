#!/usr/bin/env python3
"""
Thermal Manager — GEAR (GPU Energy-Aware Runtime)
GPU 热管理与"可回收废热"度量。

用于：温度监测、热状态分级、过热降频决策、以及"可回收热量"这一能效指标。
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional


class ThermalStatus(Enum):
    """热状态分级"""
    COOL = "cool"            # < 55°C
    NOMINAL = "nominal"     # 55-72°C
    WARM = "warm"           # 72-83°C
    HOT = "hot"             # 83-90°C
    CRITICAL = "critical"   # > 90°C


@dataclass
class ThermalState:
    """热管理系统状态"""
    gpu_temp: float = 0.0            # GPU 核心温度
    coolant_temp: float = 0.0        # 冷却液温度
    heat_recovery_rate_w: float = 0.0  # 可回收废热功率 (W)
    coolant_flow_rate_lpm: float = 0.0 # 冷却液流速 (L/min)
    status: ThermalStatus = ThermalStatus.COOL


class ThermalManager:
    """
    GPU 热管理 + 可回收废热度量。

    温度阈值与降温策略：
    - COOL / NOMINAL：正常
    - WARM：开始约束功耗/频率
    - HOT：强制降频降功耗
    - CRITICAL：紧急保护
    """

    T_COOL = 55.0
    T_NOMINAL = 72.0
    T_WARM = 83.0
    T_CRITICAL = 90.0

    HEAT_RECOVERY_EFFICIENCY = 0.85

    def __init__(self, gpu_index: int = 0):
        self.gpu_index = gpu_index
        self.state = ThermalState()
        self._running = False
        self._monitor_thread = None
        self._callbacks: List[Callable] = []

        # 散热/废热回收参数（研究/配置用，非宣传）
        self.thermal_spec = {
            "coolant": "dielectric fluid",
            "heat_recovery_efficiency": self.HEAT_RECOVERY_EFFICIENCY,
            "notes": "可回收废热功率为估算指标；实际利用需独立余热回收系统。",
        }

    def _classify(self, temp: float) -> ThermalStatus:
        if temp < self.T_COOL:
            return ThermalStatus.COOL
        if temp < self.T_NOMINAL:
            return ThermalStatus.NOMINAL
        if temp < self.T_WARM:
            return ThermalStatus.WARM
        if temp < self.T_CRITICAL:
            return ThermalStatus.HOT
        return ThermalStatus.CRITICAL

    def update_thermal_state(self, gpu_temp: float):
        """更新热状态并估算可回收废热。"""
        self.state.gpu_temp = gpu_temp
        self.state.coolant_temp = gpu_temp - 15.0
        self.state.status = self._classify(gpu_temp)

        # 可回收废热：假设基线 40°C 以下不可回收，其余按效率折算
        if gpu_temp > 40.0:
            delta = gpu_temp - 40.0
            self.state.heat_recovery_rate_w = delta * 5.0 * self.HEAT_RECOVERY_EFFICIENCY
        else:
            self.state.heat_recovery_rate_w = 0.0

    def thermal_guidance(self) -> dict:
        """根据当前热状态给出降频/降功耗建议。"""
        status = self.state.status
        action = {
            ThermalStatus.COOL: "低温，可放开频率",
            ThermalStatus.NOMINAL: "正常，保持能效最优策略",
            ThermalStatus.WARM: "轻微过热，建议逐步降低频率/功耗",
            ThermalStatus.HOT: "过热，立即降频并收敛功耗",
            ThermalStatus.CRITICAL: "严重过热，强制最保守配置并考虑停机",
        }[status]
        return {
            "status": status.value,
            "gpu_temp_c": self.state.gpu_temp,
            "coolant_temp_c": self.state.coolant_temp,
            "heat_recovery_w": round(self.state.heat_recovery_rate_w, 1),
            "action": action,
        }

    def control_coolant_flow(self, target_temp: float):
        """简化 PID：调节冷却液流速逼近目标温度。"""
        error = self.state.gpu_temp - target_temp
        if error > 5:
            self.state.coolant_flow_rate_lpm = min(5.0, self.state.coolant_flow_rate_lpm + 0.5)
        elif error < -5:
            self.state.coolant_flow_rate_lpm = max(0.5, self.state.coolant_flow_rate_lpm - 0.5)

    def start_monitoring(self, callback: Optional[Callable] = None):
        """启动监控线程（默认用模拟传感器，接入真实传感器请替换 read_gpu_temp）。"""
        self._running = True
        if callback:
            self._callbacks.append(callback)

        def loop():
            while self._running:
                # 模拟读温（真机请替换为 nvml 或物理传感器）
                sim = 60.0 + 20.0 * abs((time.time() % 4) - 2) / 2
                self.update_thermal_state(sim)
                for cb in self._callbacks:
                    cb(self.state)
                time.sleep(1.0)

        self._monitor_thread = threading.Thread(target=loop, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)

    def get_spec(self) -> dict:
        """返回散热/废热回收参数。"""
        return self.thermal_spec
