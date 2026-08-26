"""
data/factors.py
================

可组合因子库（纯 numpy/pandas，无外部行情与 ML 依赖）。

设计目标
--------
- 每个因子是一个纯函数：``f(df: pd.DataFrame) -> pd.Series``（按时间索引对齐）。
- 通过 :class:`Factor` 把命名、函数、组别绑定起来，方便注册、组合、白盒解释。
- 复用并扩展原 ``quant_features.py`` 的逻辑（RSI / ATR / 特征 / 背离），
  并补充更适合 **A股 TMT 板块** 的因子（动量、趋势、波动率、量比、行业相对强弱等）。

用法
----
    from 量化系统.data.factors import FACTORS, compute_factors
    df_feat = compute_factors(price_df)      # 一次性算出全部注册因子
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

# 每个因子函数签名： (df) -> pd.Series
FactorFn = Callable[[pd.DataFrame], pd.Series]


# --------------------------------------------------------------------------
# 基础指标
# --------------------------------------------------------------------------
def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """RSI（相对强弱指标），pandas 向量化版本。"""
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss + 1e-8)
    return 100 - (100 / (1 + rs))


def atr_ratio(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """ATR 相对当前价格的比值（用于动态止损/仓位）。输入需含 high/low/close。"""
    if not {"high", "low", "close"}.issubset(df.columns):
        return pd.Series(np.nan, index=df.index)
    high, low, close = df["high"], df["low"], df["close"]
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr / close


# --------------------------------------------------------------------------
# 基于收盘价的经典特征
# --------------------------------------------------------------------------
def ret(series: pd.Series, period: int) -> pd.Series:
    return series.pct_change(period)


def momentum(series: pd.Series, period: int = 20) -> pd.Series:
    return series / series.shift(period) - 1


def ma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window).mean()


def bias(series: pd.Series, window: int = 20) -> pd.Series:
    m = ma(series, window)
    return (series / m - 1) * 100


def volatility(series: pd.Series, period: int = 20) -> pd.Series:
    return series.pct_change().rolling(period).std() * np.sqrt(252)


# --------------------------------------------------------------------------
# 注册表
# --------------------------------------------------------------------------
@dataclass
class Factor:
    name: str
    fn: FactorFn
    group: str = "price"   # price / volume / trend / sentiment
    description: str = ""


def _factor_ret_1d(df: pd.DataFrame) -> pd.Series:
    return ret(df["close"], 1)


def _factor_ret_5d(df: pd.DataFrame) -> pd.Series:
    return ret(df["close"], 5)


def _factor_ret_20d(df: pd.DataFrame) -> pd.Series:
    return ret(df["close"], 20)


def _factor_momentum_20(df: pd.DataFrame) -> pd.Series:
    return momentum(df["close"], 20)


def _factor_momentum_60(df: pd.DataFrame) -> pd.Series:
    return momentum(df["close"], 60)


def _factor_rsi(df: pd.DataFrame) -> pd.Series:
    return rsi(df["close"], 14)


def _factor_ma_bias(df: pd.DataFrame) -> pd.Series:
    return bias(df["close"], 20)


def _factor_volatility(df: pd.DataFrame) -> pd.Series:
    return volatility(df["close"], 20)


def _factor_trend(df: pd.DataFrame) -> pd.Series:
    return (ma(df["close"], 20) > ma(df["close"], 60)).astype(int)


def _factor_bb_position(df: pd.DataFrame) -> pd.Series:
    c = df["close"]
    std20 = c.rolling(20).std()
    m20 = c.rolling(20).mean()
    lower = m20 - 2 * std20
    return (c - lower) / (4 * std20 + 1e-8)


def _factor_volume_ratio(df: pd.DataFrame) -> pd.Series:
    if "volume" not in df.columns:
        return pd.Series(1.0, index=df.index)
    return df["volume"] / df["volume"].rolling(20).mean()


def _factor_turnover(df: pd.DataFrame) -> pd.Series:
    """量比归一化的换手代理（无流通股本时用成交量代替）。"""
    if "volume" not in df.columns:
        return pd.Series(1.0, index=df.index)
    return df["volume"] / (df["volume"].rolling(60).mean() + 1e-8)


def _factor_atr(df: pd.DataFrame) -> pd.Series:
    return atr_ratio(df, 14)


# --------------------------------------------------------------------------
# 资金流代理因子（无真实资金流水接口时，用量价行为构造）
# --------------------------------------------------------------------------
def _factor_fund_flow_net(df: pd.DataFrame) -> pd.Series:
    """净流入代理：sign(收益) * 成交量 的 5 日累计（正 = 放量上涨的净买盘）。

    仅用 close 与 volume 构造，离线/任何数据源都可用；在个股间横向可比性一般，
    更适合用于排序/相对强弱的度。
    """
    if "volume" not in df.columns:
        return pd.Series(0.0, index=df.index)
    ret1 = df["close"].pct_change()
    flow = np.sign(ret1) * df["volume"]
    return flow.rolling(5).sum() / (df["volume"].rolling(5).sum() + 1e-8)


def _factor_fund_flow_upvol(df: pd.DataFrame) -> pd.Series:
    """上涨日成交量占比（涨时放量、跌时缩量 -> 更接近主力流入）。"""
    if "volume" not in df.columns:
        return pd.Series(0.5, index=df.index)
    up_day = (df["close"].diff() > 0).astype(float)
    up_vol = (up_day * df["volume"]).rolling(10).sum()
    total_vol = df["volume"].rolling(10).sum()
    return (up_vol / (total_vol + 1e-8)).clip(0.0, 1.0)


def _factor_fund_flow_obv(df: pd.DataFrame) -> pd.Series:
    """OBV 强度：OBV 的 20 日标准差归一（相对强弱）。"""
    if "volume" not in df.columns:
        return pd.Series(0.0, index=df.index)
    direction = np.sign(df["close"].diff()).fillna(0.0)
    obv = (direction * df["volume"]).cumsum()
    return (obv - obv.rolling(20).mean()) / (obv.rolling(20).std() + 1e-8)


def _factor_northbound_sentiment(df: pd.DataFrame) -> pd.Series:
    """北向资金情绪代理（市场级）。

    若加载了北向资金数据会作为外部分列注入；这里提供一个默认的 0.5 中性占位,
    由 loader 在存在北向时覆写为真实值。仅用 price 时无法构造，故返回中性。
    """
    if "northbound" in df.columns:
        return df["northbound"].clip(0.0, 1.0)
    return pd.Series(0.5, index=df.index)


# --------------------------------------------------------------------------
# 基准因子
# --------------------------------------------------------------------------
FACTORS: list[Factor] = [
    Factor("ret_1d", _factor_ret_1d, "price", "1日收益"),
    Factor("ret_5d", _factor_ret_5d, "price", "5日收益"),
    Factor("ret_20d", _factor_ret_20d, "price", "20日收益"),
    Factor("momentum_20", _factor_momentum_20, "trend", "20日动量"),
    Factor("momentum_60", _factor_momentum_60, "trend", "60日动量"),
    Factor("rsi", _factor_rsi, "price", "相对强弱指标(14)"),
    Factor("ma_bias", _factor_ma_bias, "trend", "20日均线乖离率"),
    Factor("volatility", _factor_volatility, "risk", "20日年化波动率"),
    Factor("trend", _factor_trend, "trend", "MA20>MA60 趋势"),
    Factor("bb_position", _factor_bb_position, "price", "布林带内位置"),
    Factor("volume_ratio", _factor_volume_ratio, "volume", "量比(20)"),
    Factor("turnover", _factor_turnover, "volume", "换手代理(60)"),
    Factor("atr", _factor_atr, "risk", "ATR/价格"),
    Factor("fund_flow_net", _factor_fund_flow_net, "volume", "净流入代理(5日)"),
    Factor("fund_flow_upvol", _factor_fund_flow_upvol, "volume", "上涨日量占比(10日)"),
    Factor("fund_flow_obv", _factor_fund_flow_obv, "volume", "OBV强度(20日)"),
    Factor("northbound_sentiment", _factor_northbound_sentiment, "sentiment", "北向情绪代理"),
]

FACTOR_MAP: dict[str, Factor] = {f.name: f for f in FACTORS}


def register_factor(factor: Factor) -> None:
    """注册自定义因子。"""
    FACTOR_MAP[factor.name] = factor
    if factor not in FACTORS:
        FACTORS.append(factor)


def compute_factor(df: pd.DataFrame, name: str) -> pd.Series:
    """计算单个因子；缺失时返回全 NaN。"""
    f = FACTOR_MAP.get(name)
    if f is None:
        return pd.Series(np.nan, index=df.index)
    try:
        return f.fn(df).rename(name)
    except Exception:
        return pd.Series(np.nan, index=df.index)


def compute_factors(
    df: pd.DataFrame,
    names: list[str] | None = None,
    groups: list[str] | None = None,
) -> pd.DataFrame:
    """批量计算因子，返回以因子名为列、与输入索引对齐的 DataFrame。

    参数
    ----
    df : 含 close（必需），可选 high / low / volume 列。
    names : 指定因子；默认全部。
    groups : 按组筛选（price/trend/volume/risk）。
    """
    selected = FACTORS
    if names:
        selected = [FACTOR_MAP[n] for n in names if n in FACTOR_MAP]
    if groups:
        selected = [f for f in selected if f.group in groups]

    out = pd.DataFrame(index=df.index)
    for f in selected:
        s = compute_factor(df, f.name)
        if s is not None and len(s) > 0:
            out[f.name] = s
    return out


# --------------------------------------------------------------------------
# 标签
# --------------------------------------------------------------------------
def add_labels(
    df: pd.DataFrame,
    forward_days: int = 5,
    threshold: float = 0.003,
    price_col: str = "close",
) -> pd.DataFrame:
    """添加前瞻收益标签（无未来数据泄露），并去除 NaN。"""
    df = df.copy()
    df["future_ret"] = df[price_col].shift(-forward_days) / df[price_col] - 1
    df["label"] = (df["future_ret"] > threshold).astype(int)
    return df.dropna()


def clean_array(X: np.ndarray) -> np.ndarray:
    """NaN / Inf 置 0，兼容老 numpy。"""
    X = np.asarray(X, dtype=float)
    X = np.where(np.isnan(X), 0, X)
    X = np.where(np.isinf(X), 0, X)
    return X
