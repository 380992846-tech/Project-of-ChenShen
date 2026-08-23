"""quant_features 纯函数单元测试（无网络 / 无外部行情依赖）。"""

from __future__ import annotations

import numpy as np
import pandas as pd

from quant_features import (
    add_labels,
    calc_atr,
    calc_rsi,
    calculate_rsi,
    check_rsi_divergence,
    clean_array,
    get_features,
)


def _series(vals):
    return pd.Series(vals, dtype="float64")


# ---------- RSI ----------
def test_calculate_rsi_bounds():
    s = _series(np.linspace(1, 100, 60))
    rsi = calculate_rsi(s, 14)
    assert rsi.dropna().between(0, 100).all()


def test_calculate_rsi_monotonic_uptrend_high():
    s = _series(np.linspace(1, 100, 40))
    rsi = calculate_rsi(s, 14).dropna()
    assert rsi.iloc[-1] > 90  # 持续上涨 → RSI 接近 100


def test_calc_rsi_insufficient_samples():
    assert calc_rsi(np.array([1.0, 2.0]), 14) == 50.0


def test_calc_rsi_constant_series_hundred():
    # 无下跌 → avg_loss=0 → RSI=100
    assert calc_rsi(np.full(30, 5.0), 14) == 100.0


# ---------- ATR ----------
def test_calc_atr_insufficient():
    assert calc_atr([1, 2, 3], [0.5, 1, 2], [1, 2, 3], 14) == 0.01


def test_calc_atr_positive():
    high = np.array([10, 11, 12, 13, 14, 15])
    low = np.array([9, 10, 11, 12, 13, 14])
    close = np.array([9.5, 10.5, 11.5, 12.5, 13.5, 14.5])
    atr = calc_atr(high, low, close, 3)
    assert atr > 0 and atr < 1


# ---------- 特征工程 ----------
def test_get_features_columns_and_no_forward_leak():
    df = pd.DataFrame({
        "price": np.linspace(10, 30, 80),
        "volume": np.linspace(100, 200, 80),
    })
    out = get_features(df)
    for col in ("ret_1d", "ma20", "ma60", "bias", "vol_ratio", "volatility", "rsi", "trend"):
        assert col in out.columns
    # 未来数据不得出现在历史行（ret_5d 前 5 行为 NaN）
    assert out["ret_5d"].iloc[:5].isna().all()


# ---------- 标签 ----------
def test_add_labels_drops_nan_and_sets_0_1():
    df = pd.DataFrame({"price": np.linspace(10, 30, 80)})
    out = add_labels(df, forward_days=5, threshold=0.005)
    assert set(out["label"].unique()) <= {0, 1}
    assert not out["label"].isna().any()


# ---------- 清洗 ----------
def test_clean_array():
    x = np.array([1.0, np.nan, np.inf, -np.inf, 3.0])
    assert np.array_equal(clean_array(x), np.array([1.0, 0.0, 0.0, 0.0, 3.0]))


# ---------- 背离 ----------
def test_check_rsi_divergence_detects():
    # 价格创新低，但 RSI 更高 → 底背离
    close = np.array([10, 9, 8, 7, 6, 5, 4])
    rsi = np.array([50, 48, 45, 40, 38, 42, 41])  # 低点 RSI 抬高
    assert check_rsi_divergence(close, rsi, lookback=7) is True


def test_check_rsi_divergence_false_when_short():
    assert check_rsi_divergence(np.array([1, 2]), np.array([1, 2]), lookback=20) is False
