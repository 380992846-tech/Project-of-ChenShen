"""
strategy/tmt_rotation.py
=========================

A股 TMT 板块轮动策略（默认策略）。

逻辑概要
--------
1. 每个 TMT 子行业标的计算趋势与动量：
   - 趋势过滤：close > MA(``trend_window``)，避免逆势买入；
   - 动量排序：按 ``momentum_window`` 日收益率排序，取前 ``top_n`` 名。
2. 入选标的按「波动率倒数」加权（风险平价思想），并归一化到总仓位。
3. 若持有标的跌破趋势线（或动量跌出前 ``top_n * 2``），权重置 0 退出。

输出为每根 bar 的目标权重矩阵，交给回测引擎撮合、风控约束、执行层下单。
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from 量化系统.data.loader import PricePanel
from 量化系统.data.factors import ma, momentum, volatility, compute_factor
from 量化系统.strategy.base import BaseStrategy, normalize_weights, to_target_positions


class TMTRotationStrategy(BaseStrategy):
    """TMT 板块动量轮动。"""

    name = "tmt_rotation"

    def init(self) -> None:
        scfg = self.settings.strategy
        self.momentum_window = int(self.params.get("momentum_window", scfg.momentum_window))
        self.trend_window = int(self.params.get("trend_window", scfg.trend_window))
        self.top_n = int(self.params.get("top_n", scfg.top_n))
        self.max_position = float(self.settings.risk.max_position)
        self.target_vol = float(self.settings.risk.target_vol)
        # 复合 alpha：0 = 纯动量；>0 则融入资金流/OBV 强度做排序
        self.fund_flow_weight = float(self.params.get("fund_flow_weight", 0.0))

    def _fund_flow_score(self, panel: PricePanel) -> pd.DataFrame:
        """资金流/量能强度矩阵，按每行分位归一（0..1），保证跨标的可比。"""
        score = pd.DataFrame(0.0, index=panel.close.index, columns=panel.symbols)
        for sym in panel.symbols:
            df = panel.per_symbol.get(sym)
            if df is None:
                continue
            obv = compute_factor(df, "fund_flow_obv")
            upvol = compute_factor(df, "fund_flow_upvol")
            net = compute_factor(df, "fund_flow_net")
            raw = 0.5 * obv.fillna(0.0) + 0.3 * (upvol.fillna(0.5) - 0.5) + 0.2 * net.fillna(0.0)
            score[sym] = raw
        # 每行分位归一（0..1）
        return score.rank(axis=1, pct=True).clip(0.0, 1.0).fillna(0.5)

    def generate_signals(self, panel: PricePanel) -> pd.DataFrame:
        close = panel.close
        if close.empty:
            return pd.DataFrame()

        # 趋势过滤：close > MA；动量：window 日收益率；波动率用于权重
        trend_ok = close > ma(close, self.trend_window)
        mom = momentum(close, self.momentum_window)
        vol = volatility(close, 20).replace(0.0, np.nan).fillna(self.target_vol)

        # 资金流/量能强度（若启用）
        if self.fund_flow_weight > 0:
            flow_score = self._fund_flow_score(panel)
            # 动量分位归一
            mom_rank = mom.rank(axis=1, pct=True).fillna(0.5)
            blend = (1 - self.fund_flow_weight) * mom_rank + self.fund_flow_weight * flow_score
        else:
            blend = mom.rank(axis=1, pct=True).fillna(0.5)

        # 在满足趋势的标的中保留复合分数，其余置 NaN；再按行降序排名
        scores = blend.where(trend_ok & mom.notna(), np.nan)
        rank = scores.rank(axis=1, ascending=False, method="first", na_option="keep")
        # 只保留排名 <= top_n 的标的
        selected = (rank <= self.top_n) & scores.notna()

        # 选中标的按波动率倒数加权
        inv_vol = 1.0 / vol
        raw_weights = inv_vol.where(selected, 0.0)
        row_sum = raw_weights.sum(axis=1)
        row_sum = row_sum.replace(0.0, np.nan)
        weights = raw_weights.div(row_sum, axis=0).fillna(0.0)

        # 总仓位上限
        pos = to_target_positions(weights, self.max_position)

        # 交易流水（信号变化位置；离线环境不生成，避免刷日志）
        if panel.settings.environment != "offline":
            changes = (pos - pos.shift(1).fillna(0.0))
            change_mask = changes.abs() > 1e-6
            for ts, row in change_mask.iterrows():
                for sym in row.index:
                    if row[sym]:
                        delta = changes.loc[ts, sym]
                        self.on_trade(sym, "buy" if delta > 0 else "sell",
                                      float(close.loc[ts, sym]))
        return pos


# 便捷别名，兼容旧策略脚本命名
TMTQQ = TMTRotationStrategy
