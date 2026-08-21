"""首轮单元测试：覆盖 `大模型/量化策略（聚宽·回测）/quant_features.py` 的纯函数逻辑。"""

import numpy as np
import pandas as pd
import pytest
from quant_features import (
    add_labels,
    calc_atr,
    calc_rsi,
    calculate_rsi,
    check_rsi_divergence,
    clean_array,
    get_features,
)


# --------------------------------------------------------------------------
# RSI
# --------------------------------------------------------------------------
def test_calculate_rsi_bounds():
    """RSI 应落在 [0, 100] 区间内。"""
    prices = pd.Series(np.linspace(1.0, 200.0, 500))
    rsi = calculate_rsi(prices, period=14).dropna()
    assert rsi.min() >= 0.0
    assert rsi.max() <= 100.0


def test_calc_rsi_insufficient_data_returns_neutral():
    """样本不足时返回中性值 50。"""
    assert calc_rsi(np.array([1.0, 2.0]), period=14) == 50.0


def test_calc_rsi_all_gains_is_100():
    """持续上涨时应返回 100。"""
    prices = np.arange(1.0, 60.0, dtype=float)
    assert calc_rsi(prices, period=14) == pytest.approx(100.0)


# --------------------------------------------------------------------------
# ATR
# --------------------------------------------------------------------------
def test_calc_atr_positive():
    """正常输入下 ATR 比值应为正。"""
    high = np.array([10.0, 11.0, 12.0, 13.0, 14.0, 15.0])
    low = np.array([9.0, 9.5, 10.0, 10.5, 11.0, 11.5])
    close = np.array([9.5, 10.5, 11.5, 12.5, 13.5, 14.5])
    assert calc_atr(high, low, close, period=5) > 0.0


def test_calc_atr_insufficient_data():
    """样本不足时返回保守值 0.01。"""
    assert calc_atr(np.array([1.0]), np.array([1.0]), np.array([1.0])) == 0.01


# --------------------------------------------------------------------------
# 特征工程
# --------------------------------------------------------------------------
def test_get_features_columns():
    """特征工程应产出预期列。"""
    n = 120
    df = pd.DataFrame(
        {
            "price": np.linspace(10.0, 20.0, n) + np.random.randn(n) * 0.01,
            "volume": np.linspace(1000.0, 2000.0, n),
        }
    )
    out = get_features(df)
    for col in [
        "ret_1d",
        "ret_5d",
        "ret_20d",
        "ma20",
        "ma60",
        "bias",
        "vol_ratio",
        "volatility",
        "rsi",
        "trend",
    ]:
        assert col in out.columns


def test_add_labels_no_future_leak():
    """标签由 ``shift(-forward_days)`` 生成，不应包含 NaN。"""
    df = pd.DataFrame({"price": np.linspace(1.0, 100.0, 200)})
    labeled = add_labels(df, forward_days=5, threshold=0.005)
    assert "label" in labeled.columns
    assert labeled["label"].isin([0, 1]).all()
    assert not labeled["future_ret"].isna().any()


def test_clean_array_removes_nan_inf():
    """NaN / Inf 应被替换为 0。"""
    x = np.array([[np.nan, np.inf], [1.0, -np.inf]])
    cleaned = clean_array(x)
    assert np.isfinite(cleaned).all()
    assert cleaned[0, 0] == 0.0


# --------------------------------------------------------------------------
# RSI 背离
# --------------------------------------------------------------------------
def test_check_rsi_divergence_detects_bottom():
    """价格创新低但 RSI 创新高的低点：应判定为底背离。"""
    # 最后收盘价(3.9)创新低，但对应 RSI(30) 高于此前的 RSI 低点(20 @ 4.0)
    close = np.array([10, 9, 8, 7, 6, 5, 4, 3.9])
    rsi = np.array([60, 55, 50, 45, 40, 35, 20, 30])
    assert check_rsi_divergence(close, rsi, lookback=8) is True


def test_check_rsi_divergence_no_signal_when_lows_coincide():
    """价格低点与 RSI 低点重合时，不应判定为底背离。"""
    close = np.array([10, 9, 8, 7, 6, 5, 4, 4.1])
    rsi = np.array([60, 55, 50, 45, 40, 35, 30, 45])
    assert check_rsi_divergence(close, rsi, lookback=8) is False


def test_check_rsi_divergence_short_series():
    """序列过短时应返回 False 而不抛异常。"""
    assert check_rsi_divergence(np.array([1.0, 2.0]), np.array([50.0, 60.0])) is False
