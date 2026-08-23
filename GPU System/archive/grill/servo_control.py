#!/usr/bin/env python3
"""
Servo Control for Auto Flip
自动翻面伺服控制接口。默认每 45s 翻转 90 度。
"""

import time


class ServoControl:
    """自动翻面舵机控制器"""

    def __init__(self, simulate: bool = True, pin: int = 13):
        self.simulate = simulate
        self.pin = pin
        self.flip_interval = 45  # 秒
        self._last_flip = time.time()

    def _pulse(self, angle: int):
        """实际驱动 GPIO（RPi.GPIO / Adafruit ServoKit）"""
        raise NotImplementedError("接入实际舵机库：RPi.GPIO + PWM 或 Adafruit PCA9685")

    def maybe_flip(self) -> str:
        """到达翻面间隔则触发一次翻转，返回动作描述"""
        if time.time() - self._last_flip >= self.flip_interval:
            self._last_flip = time.time()
            angle = 90
            if not self.simulate:
                self._pulse(angle)
            return f"🔄 自动翻面 -> {angle}°"
        return ""

    def force_flip(self, angle: int = 90) -> str:
        """手动强制翻面"""
        self._last_flip = time.time()
        if not self.simulate:
            self._pulse(angle)
        return f"🔄 强制翻面 -> {angle}°"
