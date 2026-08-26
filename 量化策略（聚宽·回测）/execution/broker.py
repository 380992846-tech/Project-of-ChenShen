"""
execution/broker.py
===================

执行层抽象：统一的券商/模拟接口。

设计目标
--------
- 定义下单/撤单/查仓/查资产的最小接口，让「模拟」和「实盘」可互换。
- 与风控、策略解耦：策略只管出目标权重，Broker 负责成交与持仓。
- 所有实现应可逆、可测试；实盘适配器必须在模拟环境先行验证。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Order:
    """一笔订单（客户端视角）。"""
    symbol: str
    side: str = "buy"            # buy / sell
    quantity: float = 0.0        # 股数
    order_type: str = "market"   # market / limit
    limit_price: float | None = None
    reason: str | None = None
    order_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "side": self.side,
            "quantity": self.quantity,
            "order_type": self.order_type,
            "limit_price": self.limit_price,
            "reason": self.reason,
            "order_id": self.order_id,
        }


@dataclass
class Position:
    symbol: str
    quantity: float = 0.0
    avg_price: float = 0.0
    market_price: float = 0.0

    @property
    def market_value(self) -> float:
        return self.quantity * self.market_price


@dataclass
class Account:
    cash: float = 0.0
    positions: list[Position] = field(default_factory=list)

    @property
    def total_value(self) -> float:
        return self.cash + sum(p.market_value for p in self.positions)


class BaseBroker(ABC):
    """所有 Broker 的抽象基类。"""

    name: str = "base"

    @abstractmethod
    def connect(self) -> None:
        """建立连接（模拟/实盘握手）。"""

    @abstractmethod
    def place_order(self, order: Order) -> dict[str, Any]:
        """下单，返回成交回报 dict。"""

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """撤单。"""

    @abstractmethod
    def get_positions(self) -> list[Position]:
        """查询持仓。"""

    @abstractmethod
    def get_account(self) -> Account:
        """查询账户资产。"""

    @abstractmethod
    def get_quote(self, symbol: str) -> float:
        """查询最新价。"""

    def disconnect(self) -> None:  # pragma: no cover - 可空实现
        pass

    def __repr__(self) -> str:  # pragma: no cover - 展示用
        return f"<{type(self).__name__} name={self.name}>"
