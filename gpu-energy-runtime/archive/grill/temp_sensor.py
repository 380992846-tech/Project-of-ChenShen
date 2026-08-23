#!/usr/bin/env python3
"""
Grill Temperature Sensor Interface
烤架温度传感器接口（IR 热电堆）。无真实硬件时返回模拟值。
"""

import time
import random


class TempSensor:
    """红外测温传感器接口"""

    def __init__(self, simulate: bool = True, port: str = "/dev/ttyUSB0"):
        self.simulate = simulate
        self.port = port
        self._last = 65.0

    def read_grill_temp(self) -> float:
        """读取烤架表面温度 (°C)"""
        if self.simulate:
            # 模拟：缓慢向上漂移 + 轻微抖动，并偶发"翻面瞬间温度略降"
            self._last += random.uniform(-0.6, 1.1)
            self._last = max(30.0, min(95.0, self._last))
            return round(self._last, 1)
        raise NotImplementedError("请接入真实 IR 传感器驱动（如 mlx90614 / AMG8833）")

    def read_food_temp(self) -> float:
        """读取食物核心温度 (°C)"""
        # 食物中心温度通常比烤架低 15-25°C
        return round(self.read_grill_temp() - random.uniform(15, 25), 1)
