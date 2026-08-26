"""
risk/manager.py
===============

风控层：事前（pre-trade）、事中（in-trade）、事后（post-trade）三层风控。

- **事前**：在策略产出目标权重后，做仓位/集中度/波动约束，输出最终可执行权重。
- **事中**：在回测逐 bar 运行中对组合做波动率压缩与最大回撤熔断。
- **事后**：基于回测结果做绩效归因/风险暴露统计。

本模块尽量把「风控约束」做成独立的、可测试的纯函数；对权重矩阵操作。
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from 量化系统.config import get_settings
from 量化系统.data.loader import PricePanel
from 量化系统.backtest.metrics import drawdown_series


# --------------------------------------------------------------------------
# 事前风控
# --------------------------------------------------------------------------
class PreTradeRisk:
    """对目标权重做约束：单标的上限、总仓位上限、波动率压制。"""

    def __init__(self, settings: Any = None):
        s = settings or get_settings()
        self.max_position = float(s.risk.max_position)
        self.per_name_limit = float(s.risk.per_name_limit)
        self.vol_cap = float(s.risk.vol_cap)
        self.target_vol = float(s.risk.target_vol)

    def apply(self, weights: pd.DataFrame, panel: PricePanel) -> pd.DataFrame:
        w = weights.fillna(0.0).clip(lower=0.0)

        # 1) 单标的集中度上限：对单行最大权重超限的行，整体按比例压到 per_name_limit
        row_max = w.max(axis=1)
        over = row_max.where(row_max > self.per_name_limit, np.nan)
        factor = (self.per_name_limit / over).fillna(1.0)  # 超限行 <1，其余 =1
        w = w.mul(factor, axis=0)

        # 2) 波动率压缩：若标的历史波动超过 vol_cap，按比例缩减该标的所有列
        vol = panel.returns.rolling(20).std() * np.sqrt(252)
        vol_recent = vol.iloc[-1].replace(0.0, np.nan)
        vol_scale = {}
        for sym in panel.symbols:
            v = vol_recent.get(sym, self.target_vol)
            if pd.isna(v):
                v = self.target_vol
            vol_scale[sym] = min(1.0, self.vol_cap / max(v, 1e-6))
        w = w.mul(pd.Series(vol_scale), axis=1)

        # 3) 总仓位上限
        row_sum = w.sum(axis=1)
        over = row_sum.where(row_sum > self.max_position, np.nan)
        w = w.div(over, axis=0).fillna(w)
        return w.clip(lower=0.0).fillna(0.0)


# --------------------------------------------------------------------------
# 事中风控
# --------------------------------------------------------------------------
class InTradeRisk:
    """事中（在交易过程中）的实时风险约束。

    升级说明
    --------
    原实现只对「回测尾部」做一次性的回撤归零，不能真正代表交易全程。这里改为
    **前视安全的逐 bar 风控覆盖层**：

    1. 用「事前风控后的目标权重」与持仓收益推算一条**临时净值**（使用 ``shift(1)``，
       即当日用昨日的目标仓位，避免用当天收盘做当天决策的未来函数）。
    2. **波动率自适应仓位**：按 ``target_vol / trailing_vol`` 缩放每 bar 总仓位，
       实现实时波动率目标（只用历史滚动波动，无前视）。
    3. **回撤熔断 + 恢复**：临时净值滚动回撤一旦超过 ``max_drawdown_halt``，把仓位
       降到 ``halt_scale``（默认 0）；当回撤恢复到 ``recover_ratio * halt`` 以上时恢复
       到正常缩放，带滞后避免来回抖动。
    4. 最后再施加总仓位上限。

    该覆盖层只在 0..1 之间缩放权重，不会放大仓位，故不引入额外杠杆风险。
    """

    def __init__(self, settings: Any = None, max_drawdown_halt: float | None = None):
        s = settings or get_settings()
        self.max_position = float(s.risk.max_position)
        self.target_vol = float(s.risk.target_vol)
        self.max_drawdown_halt = (
            s.risk.max_drawdown_halt if max_drawdown_halt is None else max_drawdown_halt
        )
        self.vol_lookback = int(s.risk.vol_lookback if hasattr(s.risk, "vol_lookback") else 20)
        self.vol_floor = float(s.risk.vol_floor if hasattr(s.risk, "vol_floor") else 0.20)
        self.halt_scale = float(s.risk.halt_scale if hasattr(s.risk, "halt_scale") else 0.0)
        # 回撤恢复到该比例以上才解除熔断（滞后）
        self.recover_ratio = float(s.risk.recover_ratio if hasattr(s.risk, "recover_ratio") else 0.5)

    def constrain(
        self,
        target: pd.DataFrame,
        nav: pd.Series | None = None,
        panel: PricePanel | None = None,
    ) -> pd.DataFrame:
        """对目标权重做事中实时约束。

        ``panel`` 提供时启用波动率自适应 + 回撤熔断/恢复（推荐，真正"在交易中"）。
        仅提供 ``nav`` 时退化为简单回撤熔断（兼容旧用法）。
        """
        w = target.fillna(0.0).clip(lower=0.0)
        if panel is not None:
            mult = self._multiplier_series(target, panel)
            w = w.mul(mult, axis=0)
        elif nav is not None and len(nav) > 1:
            mult = self._drawdown_multiplier(nav)
            w = w.mul(mult, axis=0)

        # 总仓位上限
        row_sum = w.sum(axis=1)
        over = row_sum.where(row_sum > self.max_position, np.nan)
        w = w.div(over, axis=0).fillna(w)
        return w

    # ------------------------------------------------------------------
    def _provisional_returns(self, target: pd.DataFrame, panel: PricePanel) -> pd.Series:
        """用「昨日目标仓位」的持仓收益推算当日组合收益（前视安全）。"""
        pos = target.shift(1).fillna(0.0)
        ret = (pos * panel.returns).sum(axis=1)
        return ret.fillna(0.0)

    def _multiplier_series(self, target: pd.DataFrame, panel: PricePanel) -> pd.Series:
        """返回每 bar 的风控缩放系数（0..1），由波动率自适应 + 回撤熔断/恢复决定。"""
        r = self._provisional_returns(target, panel)
        nav = (1 + r).cumprod()
        pos_vol = self._trailing_vol(r)
        dd = drawdown_series(nav)

        mult = pd.Series(1.0, index=target.index)
        # 波动率自适应：过高则降仓（floor 保底）
        vol_mult = (self.target_vol / pos_vol).clip(lower=self.vol_floor, upper=1.0)
        mult = mult * vol_mult

        # 回撤熔断/恢复（带滞后）
        halt = abs(self.max_drawdown_halt)
        breach = dd <= -halt
        state_down = False
        gate = pd.Series(1.0, index=target.index)
        for i, ts in enumerate(target.index):
            dd_val = dd.iloc[i]
            if not state_down:
                if dd_val <= -halt:
                    state_down = True
            else:
                # 若回撤恢复到阈值的一半以上，解除熔断
                if dd_val > -halt * self.recover_ratio:
                    state_down = False
            gate.iloc[i] = self.halt_scale if state_down else 1.0
        return (mult * gate).clip(0.0, 1.0)

    @staticmethod
    def _trailing_vol(returns: pd.Series, lookback: int = 20) -> pd.Series:
        """历史滚动年化波动率（只用过去 lookback 天）。"""
        v = returns.rolling(lookback).std() * np.sqrt(252)
        return v.replace(0.0, np.nan).fillna(0.30)

    def _drawdown_multiplier(self, nav: pd.Series) -> pd.Series:
        """仅提供净值的简单回撤熔断（兼容旧用法）。"""
        dd = drawdown_series(nav)
        halt = abs(self.max_drawdown_halt)
        breach = dd <= -halt
        mult = pd.Series(1.0, index=nav.index)
        mult[breach] = self.halt_scale
        return mult


# --------------------------------------------------------------------------
# 事后风控 / 归因
# --------------------------------------------------------------------------
class PostTradeRisk:
    """事后统计：持仓集中度、行业暴露、最大回撤归因等。"""

    def __init__(self, settings: Any = None):
        self.settings = settings or get_settings()

    def exposure_report(self, holdings: pd.DataFrame) -> dict:
        """基于最终持仓市值统计集中度与行业暴露。"""
        # 行业分组
        sym_group = self.settings.universe_flat
        last = holdings.iloc[-1] if len(holdings) else pd.Series(dtype=float)
        industry: dict[str, float] = {}
        total = last.sum()
        for sym, val in last.items():
            if val > 0:
                g = sym_group.get(sym, "其他")
                industry[g] = industry.get(g, 0.0) + float(val)
        industry_pct = {k: (v / total if total > 0 else 0.0) for k, v in industry.items()}
        return {
            "industry_exposure": {k: round(v, 4) for k, v in industry_pct.items()},
            "num_positions": int((last > 0).sum()),
            "top_position": round(float(last.max()) / total, 4) if total > 0 else 0.0,
            "total_value": float(total),
        }


# --------------------------------------------------------------------------
# 统一风控入口
# --------------------------------------------------------------------------
class RiskManager:
    """把三层风控串起来的门面，供 service/orchestrator 使用。"""

    def __init__(self, settings: Any = None):
        self.settings = settings or get_settings()
        self.pre = PreTradeRisk(self.settings)
        self.intrade = InTradeRisk(self.settings)
        self.post = PostTradeRisk(self.settings)

    def pre_trade(self, weights: pd.DataFrame, panel: PricePanel) -> pd.DataFrame:
        return self.pre.apply(weights, panel)

    def in_trade(self, target: pd.DataFrame, nav: pd.Series | None = None,
                 panel: PricePanel | None = None) -> pd.DataFrame:
        return self.intrade.constrain(target, nav=nav, panel=panel)

    def post_trade(self, holdings: pd.DataFrame) -> dict:
        return self.post.exposure_report(holdings)
