"""
execution/simulated.py
=======================

模拟交易器 SimulatedBroker：无滑点/无手续费的理想化测试（可配置成本）。

- 维护现金与持仓；成交按给定 fill price 全额即时撮合。
- 用于策略/风控的正确性验证与离线演示。
"""

from __future__ import annotations

import itertools
from typing import Any

from 量化系统.execution.broker import BaseBroker, Order, Position, Account


class SimulatedBroker(BaseBroker):
    name = "simulated"

    def __init__(self, initial_cash: float = 1_000_000.0, commission: float = 0.0,
                 slippage: float = 0.0):
        self.commission = commission
        self.slippage = slippage
        self._orders = itertools.count(1)
        self._positions: dict[str, Position] = {}
        self._cash = initial_cash
        self._initial_cash = initial_cash

    def connect(self) -> None:
        self._positions = {}
        self._cash = self._initial_cash

    def place_order(self, order: Order) -> dict[str, Any]:
        fill_price = self._fill_price(order)
        qty = order.quantity if order.side == "buy" else -order.quantity
        notional = abs(qty) * fill_price
        cost = notional * (self.commission if order.side == "buy" else self.commission + self.slippage)

        if order.side == "buy":
            if notional > self._cash:
                raise ValueError("现金不足，订单被拒")
            self._cash -= notional + cost
        else:
            self._cash += notional - cost

        pos = self._positions.get(order.symbol, Position(order.symbol))
        pos.market_price = fill_price
        if order.side == "buy":
            pos.avg_price = (pos.avg_price * pos.quantity + fill_price * qty) / (pos.quantity + qty)
            pos.quantity += qty
        else:
            pos.quantity += qty  # negative
            if pos.quantity <= 1e-6:
                self._positions.pop(order.symbol, None)
            else:
                self._positions[order.symbol] = pos
        if pos.quantity != 0:
            self._positions[order.symbol] = pos

        order_id = f"SIM-{next(self._orders):06d}"
        return {
            "order_id": order_id,
            "symbol": order.symbol,
            "side": order.side,
            "fill_price": fill_price,
            "quantity": order.quantity,
            "status": "filled",
            "commission": round(cost, 4),
        }

    def _fill_price(self, order: Order) -> float:
        base = order.limit_price or self.get_quote(order.symbol)
        # 简化：无滑点；如需可按 order.side 加减
        return base

    def cancel_order(self, order_id: str) -> bool:
        return False  # 模拟即时成交，无可撤单

    def get_positions(self) -> list[Position]:
        return list(self._positions.values())

    def get_account(self) -> Account:
        return Account(cash=self._cash, positions=list(self._positions.values()))

    def get_quote(self, symbol: str) -> float:
        # 模拟环境下需要外部注入报价；这里抛错提示由外部提供
        raise NotImplementedError(
            "SimulatedBroker 的 get_quote 需要外部行情源注入报价；回测请用 backtest 引擎。"
        )
