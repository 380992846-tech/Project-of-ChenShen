"""
backtest/metrics.py
===================

绩效指标库：收益、年化、波动、夏普、回撤、胜率、盈亏比等。

输入约定：统一接收**净值序列** ``nav: pd.Series`` 与可选的日收益 ``returns: pd.Series``。
所有函数纯函数，便于单测与组合。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from 量化系统.config import get_settings


def daily_returns(nav: pd.Series) -> pd.Series:
    return nav.pct_change().dropna()


def total_return(nav: pd.Series) -> float:
    if len(nav) < 2 or nav.iloc[0] == 0:
        return 0.0
    return float(nav.iloc[-1] / nav.iloc[0] - 1)


def annualized_return(nav: pd.Series, periods_per_year: int = 252) -> float:
    if len(nav) < 2 or nav.iloc[0] <= 0:
        return 0.0
    years = len(nav) / periods_per_year
    if years <= 0:
        return 0.0
    return float((nav.iloc[-1] / nav.iloc[0]) ** (1 / years) - 1)


def annualized_vol(returns: pd.Series, periods_per_year: int = 252) -> float:
    if len(returns) < 2 or returns.std() == 0:
        return 0.0
    return float(returns.std() * np.sqrt(periods_per_year))


def sharpe_ratio(
    nav: pd.Series,
    risk_free_rate: float | None = None,
    periods_per_year: int = 252,
) -> float:
    settings = get_settings()
    rf = risk_free_rate if risk_free_rate is not None else settings.backtest.risk_free_rate
    r = daily_returns(nav)
    if len(r) < 2 or r.std() == 0:
        return 0.0
    excess = r - rf / periods_per_year
    return float(np.sqrt(periods_per_year) * excess.mean() / r.std())


def drawdown_series(nav: pd.Series) -> pd.Series:
    cummax = nav.expanding().max()
    return nav / cummax - 1


def max_drawdown(nav: pd.Series) -> float:
    dd = drawdown_series(nav)
    return float(dd.min()) if len(dd) else 0.0


def max_drawdown_duration(nav: pd.Series) -> int:
    """最大回撤持续天数（从峰值到恢复）。"""
    dd = drawdown_series(nav)
    if len(dd) == 0:
        return 0
    trough = dd.idxmin()
    # 找峰值
    peak_nav = nav.loc[:trough].expanding().max()
    peak_date = peak_nav.idxmax()
    # 找恢复点
    recovery = nav[trough:][nav[trough:] >= peak_nav.max()]
    if len(recovery) == 0:
        return int((trough - peak_date).days)
    return int((recovery.index[0] - peak_date).days)


def win_rate(returns: pd.Series) -> float:
    if len(returns) == 0:
        return 0.0
    return float((returns > 0).sum() / len(returns))


def profit_factor(returns: pd.Series) -> float:
    """毛盈利 / 毛亏损（>1 说明净盈利）。"""
    gains = returns[returns > 0].sum()
    losses = -returns[returns < 0].sum()
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return float(gains / losses)


def calmar_ratio(nav: pd.Series) -> float:
    mdd = abs(max_drawdown(nav))
    if mdd == 0:
        return 0.0
    return float(annualized_return(nav) / mdd)


def summary_metrics(nav: pd.Series, freq: str = "daily") -> dict[str, float]:
    """一次性返回常用绩效指标字典。"""
    r = daily_returns(nav)
    periods = 252 if freq in ("daily", "D") else 52
    return {
        "total_return": total_return(nav),
        "annual_return": annualized_return(nav, periods),
        "annual_vol": annualized_vol(r, periods),
        "sharpe": sharpe_ratio(nav, periods_per_year=periods),
        "max_drawdown": max_drawdown(nav),
        "max_drawdown_duration": max_drawdown_duration(nav),
        "win_rate": win_rate(r),
        "profit_factor": profit_factor(r),
        "calmar": calmar_ratio(nav),
        "n_days": int(len(nav)),
    }
