"""
strategy/base.py
================

策略抽象基类（统一接口）。

设计目标
--------
- 所有策略继承 :class:`BaseStrategy`，实现统一生命周期：
  ``__init__`` -> ``init`` -> ``on_data``（可选）-> ``generate_signals`` -> ``on_trade``（可选）。
- 策略输出的是**每根 bar 的目标权重向量**（weight matrix，行=时间，列=标的）。
  这样可以把「信号」与「仓位/交易/风控」解耦，利于复用和测试。
- 不依赖具体数据源；数据来自 :class:`量化系统.data.loader.PricePanel`。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import pandas as pd

from 量化系统.data.loader import PricePanel


class BaseStrategy(ABC):
    """策略基类。

    子类需实现 :meth:`generate_signals`。常见的 `init` / `on_data` / `on_trade`
    是可选的钩子，默认空实现。

    持久状态（如持仓、入场价）建议放在 ``self.state`` 字典里，不要用聚类全局变量，
    以便同一个策略实例在多标的/多次运行时互相隔离。
    """

    name: str = "base"

    def __init__(self, settings: Any, **kwargs: Any):
        self.settings = settings
        self.params: dict[str, Any] = dict(kwargs)
        self.state: dict[str, Any] = {}
        self.tradelog: list[dict[str, Any]] = []
        self.init()

    # ------------------------------------------------------------------
    # 生命周期钩子
    # ------------------------------------------------------------------
    def init(self) -> None:
        """初始化，读取配置到 self.params / self.state。子类覆盖。"""

    def on_data(self, panel: PricePanel) -> None:
        """在生成信号前调用，可选预处理。覆盖。"""

    # ------------------------------------------------------------------
    # 核心：生成信号
    # ------------------------------------------------------------------
    @abstractmethod
    def generate_signals(self, panel: PricePanel) -> pd.DataFrame:
        """返回权重矩阵 DataFrame：行=bar 索引，列=标的（symbol），值∈[-1,1]。

        对于纯做多的 A 股，值域通常 [0,1]。子类实现。
        """

    # ------------------------------------------------------------------
    # 交易回调
    # ------------------------------------------------------------------
    def on_trade(self, symbol: str, action: str, price: float, reason: str | None = None) -> None:
        """可选：每笔交易触发（用于 API 实时流水、日志）。覆盖。"""
        self.tradelog.append(
            {
                "symbol": symbol,
                "action": action,
                "price": price,
                "reason": reason,
                "ts": None,
            }
        )

    def __repr__(self) -> str:  # pragma: no cover - 展示用
        return f"<{type(self).__name__} name={self.name} params={self.params}>"


# --------------------------------------------------------------------------
# 工具函数
# --------------------------------------------------------------------------
def normalize_weights(weights: pd.DataFrame) -> pd.DataFrame:
    """把权重矩阵的行做非负归一化（和为 1）；全 0 行保持 0。

    若出现负权重（做空），这里不改变，交由下级风控或限制。对纯多策略直接非负化。
    """
    w = weights.fillna(0.0).clip(lower=0.0)
    row_sum = w.sum(axis=1)
    row_sum = row_sum.replace(0.0, np.nan)
    return w.div(row_sum, axis=0).fillna(0.0)


def to_target_positions(
    weights: pd.DataFrame, max_position: float = 0.95
) -> pd.DataFrame:
    """把归一化权重缩放到总仓位上限。返回 (行=时间, 列=标的) 的目标仓位矩阵。"""
    return normalize_weights(weights).clip(upper=max_position)
