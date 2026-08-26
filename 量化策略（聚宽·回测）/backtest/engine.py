"""
backtest/engine.py
==================

向量化回测引擎。

用法
----
    result = run_backtest(panel, strategy)     # 返回 BacktestResult

- 输入：对齐的 :class:`PricePanel` + 任一 :class:`BaseStrategy`。
- 策略输出目标持仓权重矩阵，引擎以「次日换仓」模式撮合（避免用当天收盘做当天
  决策的隐含未来函数），并计入滑点/佣金/印花税。
- 输出：净值曲线、每日收益、逐标的持仓、逐笔交易、绩效指标。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from 量化系统.config import get_settings
from 量化系统.data.loader import PricePanel
from 量化系统.strategy.base import BaseStrategy
from 量化系统.backtest import metrics


@dataclass
class BacktestResult:
    settings: Any
    nav: pd.Series
    returns: pd.Series
    positions: pd.DataFrame
    holdings: pd.DataFrame       # 每标的的持有市值（元）
    trades: list[dict[str, Any]]
    metrics: dict[str, float]
    initial_capital: float
    strategy_name: str = ""

    @property
    def drawdown(self) -> pd.Series:
        return metrics.drawdown_series(self.nav)


def run_backtest(
    panel: PricePanel,
    strategy: BaseStrategy,
    initial_capital: float | None = None,
    cost: dict[str, float] | None = None,
    target_weights: pd.DataFrame | None = None,
) -> BacktestResult:
    """运行向量化回测。

    参数
    ----
    panel : 对齐后的行情面板。
    strategy : 策略实例；仅用其 ``name`` 标注，并可提供 ``target_weights``。
    initial_capital : 初始资金；默认读配置。
    cost : 成本覆盖（commission / slippage / stamp_tax）。
    target_weights : 已做风控约束的目标权重矩阵；缺省则调用策略 ``generate_signals``。
    """
    settings = get_settings()
    initial_capital = initial_capital or settings.backtest.initial_capital
    bcfg = settings.backtest.cost
    cost = cost or {
        "commission": bcfg.commission,
        "slippage": bcfg.slippage,
        "stamp_tax": bcfg.stamp_tax,
    }
    commission, slippage, stamp_tax = (
        cost.get("commission", 0.0),
        cost.get("slippage", 0.0),
        cost.get("stamp_tax", 0.0),
    )

    close = panel.close
    if close.empty:
        raise ValueError("回测面板为空")

    target = target_weights if target_weights is not None else strategy.generate_signals(panel)
    # 确保 target 与 close 对齐、补零
    target = target.reindex_like(close).fillna(0.0).clip(-1.0, 1.0)

    # 次日生效（避免未来函数）：持仓 = 昨日目标
    pos = target.shift(1).fillna(0.0)
    # 当日持仓权重（对每个 bar 已确定）
    port_ret = (pos * panel.returns).sum(axis=1)

    # 交易成本：按换手率计
    turnover = (pos - pos.shift(1).fillna(0.0)).abs().sum(axis=1)
    # 卖出印花税按卖出部分计（只对 down 换手），佣金买卖双向，滑点按换手
    sell_turnover = (pos.shift(1).fillna(0.0) - pos).clip(lower=0.0).sum(axis=1)
    # 简化：cost_rate 每单位换手
    cost_rate = commission * 2 + slippage + stamp_tax * (sell_turnover / turnover.replace(0, np.nan)).fillna(0.0)
    cost_rate = cost_rate.fillna(0.0)
    total_cost = turnover * cost_rate

    net_ret = port_ret - total_cost
    nav = (1 + net_ret).cumprod() * initial_capital

    # 每日持仓市值
    holdings = pos.mul(close, axis=0)

    # 逐笔交易（发生仓位变化即成一笔）
    trades: list[dict[str, Any]] = []
    delta = pos.diff().fillna(pos)
    for ts in pos.index:
        for sym in pos.columns:
            d = delta.loc[ts, sym]
            if abs(d) > 1e-6:
                action = "buy" if d > 0 else "sell"
                trades.append(
                    {
                        "date": ts,
                        "symbol": sym,
                        "action": action,
                        "weight": float(d),
                        "price": float(close.loc[ts, sym]),
                        "notional": float(d) * nav.loc[ts] if ts in nav.index else 0.0,
                    }
                )

    result = BacktestResult(
        settings=settings,
        nav=nav,
        returns=net_ret,
        positions=pos,
        holdings=holdings,
        trades=trades,
        metrics=metrics.summary_metrics(nav),
        initial_capital=initial_capital,
        strategy_name=strategy.name,
    )
    return result


def run_benchmark(
    panel: PricePanel,
    benchmark_symbol: str | None = None,
    benchmark_close: pd.Series | None = None,
) -> pd.Series:
    """基准（买入持有某标的）净值曲线。

    优先使用显式传入的 ``benchmark_close``（例如单独拉取的沪深300），
    否则在 ``panel`` 里按 ``benchmark_symbol`` 查。
    """
    if benchmark_close is None:
        benchmark_symbol = benchmark_symbol or get_settings().market.benchmark
        close = panel.close[benchmark_symbol]
    else:
        close = benchmark_close
    if close is None or len(close) == 0:
        return pd.Series(dtype=float)
    return close / close.iloc[0] * get_settings().backtest.initial_capital
