"""
quant_features.py
==================

纯函数形式的量化特征工程与指标计算模块。

设计目标
--------
- **无 JoinQuant / 行情依赖**：只依赖 ``numpy`` / ``pandas``，可在任意环境单元测试。
- 这些函数与 ``joinquant_v18.py`` / ``quant_v21.py`` 中的实现保持一致，
  后续可将策略脚本逐步迁移到本模块，避免逻辑重复。

包含
----
- ``calculate_rsi`` / ``calc_rsi``  —— RSI（相对强弱指标）
- ``calc_atr``                    —— ATR（平均真实波幅）
- ``get_features``                —— 经典技术特征（收益率/均线/乖离/量比/波动率/RSI/趋势）
- ``add_labels``                  —— 前瞻收益率标签（无未来数据泄露）
- ``clean_array``                 —— 清理 NaN / Inf，兼容旧版 numpy
- ``check_rsi_divergence``        —— RSI 底背离检测
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# RSI
# --------------------------------------------------------------------------
def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """基于价格序列计算 RSI（pandas 版本，返回带索引的 Series）。"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / (loss + 1e-8)
    return 100 - (100 / (1 + rs))


def calc_rsi(prices: np.ndarray, period: int = 14) -> float:
    """基于价格数组计算 RSI（标量版本）。样本不足时返回 50。"""
    if len(prices) < period + 1:
        return 50.0
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return float(100 - (100 / (1 + rs)))


# --------------------------------------------------------------------------
# ATR
# --------------------------------------------------------------------------
def calc_atr(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    period: int = 14,
) -> float:
    """计算 ATR（平均真实波幅），返回相对当前价格的比值。

    样本不足或价格为 0 时返回一个保守值 0.01，避免除零。
    """
    if len(close) < period + 1:
        return 0.01

    tr1 = high[1:] - low[1:]
    tr2 = np.abs(high[1:] - close[:-1])
    tr3 = np.abs(low[1:] - close[:-1])
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    atr = np.mean(tr[-period:])
    current_price = close[-1]
    return atr / current_price if current_price > 0 else 0.01


# --------------------------------------------------------------------------
# 特征工程
# --------------------------------------------------------------------------
def get_features(df: pd.DataFrame) -> pd.DataFrame:
    """计算经典技术特征（无未来数据泄露）。

    输入的 DataFrame 需包含 ``price`` 与 ``volume`` 两列。
    输出额外列：ret_1d/5d/20d、ma20/ma60、bias、vol_ratio、volatility、rsi、trend。
    """
    df = df.copy()

    df["ret_1d"] = df["price"].pct_change(1)
    df["ret_5d"] = df["price"].pct_change(5)
    df["ret_20d"] = df["price"].pct_change(20)

    df["ma20"] = df["price"].rolling(20).mean()
    df["ma60"] = df["price"].rolling(60).mean()
    df["bias"] = (df["price"] / df["ma20"] - 1) * 100

    df["vol_ratio"] = df["volume"] / df["volume"].rolling(20).mean()
    df["volatility"] = df["ret_1d"].rolling(20).std() * np.sqrt(252)

    df["rsi"] = calculate_rsi(df["price"], 14)
    df["trend"] = (df["ma20"] > df["ma60"]).astype(int)

    return df


def add_labels(
    df: pd.DataFrame,
    forward_days: int = 5,
    threshold: float = 0.005,
) -> pd.DataFrame:
    """添加前瞻收益标签，并去除因滚动窗口产生的空行。"""
    df = df.copy()
    df["future_ret"] = df["price"].shift(-forward_days) / df["price"] - 1
    df["label"] = (df["future_ret"] > threshold).astype(int)
    return df.dropna()


def clean_array(X: np.ndarray) -> np.ndarray:
    """将数组中的 NaN / Inf 置 0，兼容旧版 numpy。"""
    X = np.where(np.isnan(X), 0, X)
    X = np.where(np.isinf(X), 0, X)
    return X


# --------------------------------------------------------------------------
# RSI 背离
# --------------------------------------------------------------------------
def check_rsi_divergence(
    close_prices: np.ndarray,
    rsi_values: np.ndarray,
    lookback: int = 20,
) -> bool:
    """检测 RSI 底背离（看涨）。

    在回看窗口内：
      - ``P_low`` / ``RSI_at_P_low``：最低收盘价，及其对应的 RSI；
      - ``RSI_low`` / ``P_at_RSI_low``：最低 RSI，及其对应的收盘价。

    当 **价格创更低的低点** 且 **RSI 同步创更高的低点** 时视为底背离：
      ``P_low < P_at_RSI_low`` 且 ``RSI_at_P_low > RSI_low``。
    """
    if len(close_prices) < lookback or len(rsi_values) < lookback:
        return False

    window_close = close_prices[-lookback:]
    window_rsi = rsi_values[-lookback:]

    price_low_idx = int(np.argmin(window_close))
    rsi_at_price_low = window_rsi[price_low_idx]

    rsi_low_idx = int(np.argmin(window_rsi))
    price_at_rsi_low = window_close[rsi_low_idx]

    return bool(
        price_low_idx != rsi_low_idx
        and window_close[price_low_idx] < price_at_rsi_low
        and rsi_at_price_low > window_rsi[rsi_low_idx]
    )
