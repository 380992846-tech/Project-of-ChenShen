"""
strategy/score_select.py
========================

针对聚宽三件套迁移的共享底座：单标的择时规则的「多标的泛化」。

聚宽原版（v18 / v21 / xgboost_shap）每次只交易**一只**标的（如 510300 / 510500）。
迁移到多标的 TMT 面板后，把它们统一为：
  - 每只标的按原生逻辑算一个得分矩阵 ``score``（越大越看多）；
  - 在每根 bar，若空仓，从满足信号的标的中挑得分最高的持有；
  - 若持仓，按各自原生规则（止损/止盈/回撤/超时/趋势走弱）决定是否退出。

子类只需实现 :meth:`asset_score` 返回得分矩阵，并可覆写
:meth:`exit_condition` / :meth:`entry_threshold`。

得益于共享的 :class:`BaseStrategy` 生命周期，这套规则可被回测引擎直接撮合，
也能被风控层继续约束。
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

import numpy as np
import pandas as pd

from 量化系统.data.loader import PricePanel
from 量化系统.strategy.base import BaseStrategy


class ScoreSelectionStrategy(BaseStrategy):
    """「挑一只持有」的多资产择时基类。

    子类实现:
      - :meth:`asset_score` : 每标的每日得分（>=:attr:`entry_threshold` 才可买入）
      - 可选覆写 :meth:`exit_condition` / :meth:`entry_threshold`
    状态用 ``self.state`` 保存（持仓、入场价、最高价、持仓天数），避免全局变量。
    """

    def init(self) -> None:
        rcfg = self.settings.risk
        self.max_position = float(self.params.get("max_position", rcfg.max_position))
        self.stop_loss = float(self.params.get("stop_loss", rcfg.stop_loss))
        self.take_profit = float(self.params.get("take_profit", rcfg.take_profit))
        self.max_hold_days = int(self.params.get("max_hold_days", rcfg.max_hold_days))
        self.trailing_stop = float(self.params.get("trailing_stop", 0.03))
        # 状态
        self.state["holding"] = None        # 当前持有的 symbol
        self.state["entry_price"] = 0.0
        self.state["highest_price"] = 0.0
        self.state["hold_days"] = 0
        self.state["fill_ts"] = None        # 最近一次开仓时间戳

    @property
    def entry_threshold(self) -> float:
        """得分达到该值才可开仓。子类可按需覆盖。"""
        return float(self.params.get("signal_threshold", 0.55))

    # ------------------------------------------------------------------
    # 子类必须实现
    # ------------------------------------------------------------------
    @abstractmethod
    def asset_score(self, panel: PricePanel) -> pd.DataFrame:
        """返回每个标的每日得分矩阵（row=bar, col=symbol）。"""

    # ------------------------------------------------------------------
    # 退出条件（可覆写）
    # ------------------------------------------------------------------
    def exit_condition(
        self,
        panel: PricePanel,
        symbol: str,
        ts,
        score_row: pd.Series | None = None,
    ) -> str | None:
        """返回退出原因字符串；不退出返回 None。

        默认含：止损 / 止盈 / 移动止损 / 超时。
        """
        price = panel.close.loc[ts, symbol]
        pnl = (price - self.state["entry_price"]) / self.state["entry_price"]
        if pnl < -self.stop_loss:
            return "stop_loss"
        if pnl > self.take_profit:
            return "take_profit"
        if self.state["highest_price"] > 0:
            drawdown = (price - self.state["highest_price"]) / self.state["highest_price"]
            if drawdown < -self.trailing_stop:
                return "trailing_stop"
        if self.state["hold_days"] >= self.max_hold_days:
            return "max_hold"
        # 趋势走弱：当前标的得分跌到阈值之下
        if score_row is not None and symbol in score_row.index:
            if score_row[symbol] < self.entry_threshold * 0.6:
                return "trend_weaken"
        return None

    # ------------------------------------------------------------------
    # 主流程
    # ------------------------------------------------------------------
    def generate_signals(self, panel: PricePanel) -> pd.DataFrame:
        score = self.asset_score(panel)
        close = panel.close
        weights = pd.DataFrame(0.0, index=close.index, columns=close.columns)

        for i in range(1, len(close)):
            ts = close.index[i]
            score_row = score.iloc[i] if len(score) else None

            if self.state["holding"] is None:
                # 空仓：挑选可买且得分最高的标的
                cand = close.columns[(score_row >= self.entry_threshold).to_numpy()] if score_row is not None else []
                if len(cand) > 0:
                    # 选得分最高；并列取波动率相对稳定的（按 panel 波动）实现确定
                    best = max(cand, key=lambda s: (float(score_row[s]), str(s)))
                    self.state["holding"] = best
                    self.state["entry_price"] = float(close.loc[ts, best])
                    self.state["highest_price"] = float(close.loc[ts, best])
                    self.state["hold_days"] = 0
                    self.state["fill_ts"] = ts
                    weights.loc[ts, best] = self.max_position
            else:
                sym = self.state["holding"]
                self.state["hold_days"] += 1
                price = float(close.loc[ts, sym])
                self.state["highest_price"] = max(self.state["highest_price"], price)
                reason = self.exit_condition(panel, sym, ts, score_row)
                if reason is not None:
                    weights.loc[ts, sym] = 0.0
                    self._log_exit(ts, sym, reason, price)
                    self.state["holding"] = None
                    self.state["entry_price"] = 0.0
                    self.state["highest_price"] = 0.0
                    self.state["hold_days"] = 0
                else:
                    weights.loc[ts, sym] = self.max_position

        return weights

    def _log_exit(self, ts, sym, reason, price):
        self.tradelog.append({
            "symbol": sym, "action": "sell", "price": price,
            "reason": reason, "ts": str(ts.date()),
        })
