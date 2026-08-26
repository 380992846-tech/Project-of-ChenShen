"""
execution/live.py
=================

实盘交易适配器骨架 LiveBroker。

说明
----
- 这是**接口骨架**，用于替换 SimulatedBroker 接入真实券商/通道。
- 实际接入时，选择一种通道并实现 :class:`BaseBroker` 的抽象方法：
  - 券商官方 API：中泰 XTP、华泰 MATIC（需券商开通、内网/VPN）
  - 第三方封装：easytrader（券商客户端自动交易）、vn.py（开源 CTP/CTP 类）
- **务必先在模拟环境运行并验证风控/订单逻辑，再做小资金实盘。**
- 本骨架不对接真实账户，所有方法抛出 NotImplementedError，避免误用。
"""

from __future__ import annotations

from typing import Any
from enum import Enum

from 量化系统.execution.broker import BaseBroker, Order, Position, Account


class Channel(str, Enum):
    XTP = "xtp"           # 中泰证券 XTP
    MATIC = "matic"       # 华泰 MATIC
    EASYTRADER = "easytrader"  # 券商客户端自动交易
    VNPY = "vnpy"         # vn.py CTP


class LiveBroker(BaseBroker):
    """实盘适配器骨架。选择 :class:`Channel` 并填充各方法。"""

    name = "live"

    def __init__(self, channel: Channel = Channel.XTP, **config: Any):
        self.channel = channel
        self.config = config
        self._connected = False

    def connect(self) -> None:
        raise NotImplementedError(
            f"实盘通道 {self.channel.value} 未实现：请在 execution/live.py 中对接券商 API。"
        )

    def place_order(self, order: Order) -> dict[str, Any]:
        raise NotImplementedError("实盘下单未实现，请在模拟环境先行验证。")

    def cancel_order(self, order_id: str) -> bool:
        raise NotImplementedError("实盘撤单未实现。")

    def get_positions(self) -> list[Position]:
        raise NotImplementedError("实盘查询持仓未实现。")

    def get_account(self) -> Account:
        raise NotImplementedError("实盘查询账户未实现。")

    def get_quote(self, symbol: str) -> float:
        raise NotImplementedError("实盘查询行情未实现。")

    def disconnect(self) -> None:
        self._connected = False
