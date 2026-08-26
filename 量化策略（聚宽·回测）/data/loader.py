"""
data/loader.py
===============

市场数据加载器：批量拉取标的 → 清洗对齐 → 因子计算。

对外主要提供：
- :func:`load_market_data` —— 返回 ``{symbol: DataFrame}``（含 close/high/low/volume + 因子列）。
- :class:`PricePanel` —— 把多个标的对齐成宽表（价格、收益、因子），供向量化策略使用。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np
import pandas as pd

from 量化系统.config import get_settings
from 量化系统.data import factors, sources as src_mod

logger = logging.getLogger(__name__)


def load_market_data(
    symbols: list[str],
    start: str | None = None,
    end: str | None = None,
    sources_priority: list[str] | None = None,
    use_cache: bool = True,
    settings: Any = None,
) -> dict[str, pd.DataFrame]:
    """按 symbol 拉取行情并计算因子。

    返回 ``{symbol: df}``，df 的列包括：
    ``open, high, low, close, volume`` 以及 ``factors.compute_factors`` 的全部因子列。
    """
    settings = settings or get_settings()
    start = start or settings.market.start_date
    end = end or settings.market.end_date
    priority = sources_priority or settings.data.sources_priority

    panel: dict[str, pd.DataFrame] = {}
    for sym in symbols:
        try:
            raw = src_mod.fetch_with_fallback(sym, start, end, priority, settings, use_cache)
            raw.index = pd.to_datetime(raw.index)
            feat = factors.compute_factors(raw)
            df = raw.join(feat, how="left")
            panel[sym] = df
        except Exception as exc:  # noqa: BLE001
            logger.warning("跳过 %s: %s", sym, exc)
    return panel


@dataclass
class PricePanel:
    """已对齐的多资产宽表。"""

    settings: Any
    close: pd.DataFrame = field(default_factory=pd.DataFrame)      # 收盘价宽表
    open_: pd.DataFrame = field(default_factory=pd.DataFrame)
    high: pd.DataFrame = field(default_factory=pd.DataFrame)
    low: pd.DataFrame = field(default_factory=pd.DataFrame)
    volume: pd.DataFrame = field(default_factory=pd.DataFrame)
    returns: pd.DataFrame = field(default_factory=pd.DataFrame)    # 日收益宽表
    # 每个标的单独的因子 DataFrame（列=因子名）
    per_symbol: dict[str, pd.DataFrame] = field(default_factory=dict)

    @property
    def symbols(self) -> list[str]:
        return list(self.close.columns)

    def price(self, symbol: str) -> pd.Series:
        return self.close[symbol]

    def factor(self, symbol: str, name: str) -> pd.Series:
        df = self.per_symbol.get(symbol)
        if df is None:
            return pd.Series(np.nan, index=self.close.index)
        return df[name] if name in df.columns else pd.Series(np.nan, index=self.close.index)


def build_panel(
    symbols: list[str],
    start: str | None = None,
    end: str | None = None,
    settings: Any = None,
    use_cache: bool = True,
) -> PricePanel:
    """加载多标的并构建对齐的 :class:`PricePanel`。"""
    settings = settings or get_settings()
    data = load_market_data(symbols, start, end, use_cache=use_cache, settings=settings)
    if not data:
        raise RuntimeError("未加载到任何标的数据，请检查数据源配置。")

    # 用公共交易日历对齐
    all_idx = None
    for df in data.values():
        all_idx = df.index if all_idx is None else all_idx.union(df.index)
    all_idx = pd.DatetimeIndex(all_idx).sort_values()

    close = pd.DataFrame({s: df["close"].reindex(all_idx) for s, df in data.items()}).ffill()
    open_ = pd.DataFrame({s: df["open"].reindex(all_idx) for s, df in data.items()}).ffill()
    high = pd.DataFrame({s: df["high"].reindex(all_idx) for s, df in data.items()}).ffill()
    low = pd.DataFrame({s: df["low"].reindex(all_idx) for s, df in data.items()}).ffill()
    volume = pd.DataFrame({s: df["volume"].reindex(all_idx) for s, df in data.items()}).fillna(0.0)
    returns = close.pct_change()

    # 北向资金情绪（市场级，广播为每标的的 northbound 列；取不到返回 None）
    northbound = _load_northbound_sentiment(settings)

    per_symbol: dict[str, pd.DataFrame] = {}
    for s, df in data.items():
        sub = df.reindex(all_idx).ffill()
        if northbound is not None:
            sub["northbound"] = northbound.reindex(all_idx).ffill().fillna(0.5)
        per_symbol[s] = sub

    return PricePanel(
        settings=settings,
        close=close,
        open_=open_,
        high=high,
        low=low,
        volume=volume,
        returns=returns,
        per_symbol=per_symbol,
    )


def _load_northbound_sentiment(settings: Any = None, use_cache: bool = True) -> pd.Series | None:
    """加载北向资金净流入并归一化成 0..1 的情绪序列（市场级）。

    只用**北向资金当日净流入**的滚动分位归一化，避免量纲影响；取不到（离线/无接口）
    返回 None，由下游退化为中性 0.5。
    """
    settings = settings or get_settings()
    if not use_cache:
        pass
    cache_dir = settings.cache_dir
    cache_path = cache_dir / "northbound_sentiment.pkl"
    if use_cache and cache_path.exists():
        try:
            import pickle
            with open(cache_path, "rb") as f:
                return pickle.load(f)
        except Exception:
            pass

    # 尝试多个北向接口（东财 stock_hsgt_hist_em 当前可通）
    series: pd.Series | None = None
    try:
        import akshare as ak
        import numpy as np

        df = ak.stock_hsgt_hist_em(symbol="北向资金")
        df.columns = [str(c) for c in df.columns]
        date_col = next((c for c in df.columns if "日期" in c), None)
        flow_col = next((c for c in df.columns if "净流入" in c or "资金净" in c), None)
        if date_col and flow_col:
            s = pd.Series(pd.to_numeric(df[flow_col], errors="coerce").values,
                          index=pd.to_datetime(df[date_col])).sort_index()
            s = s[s.notna()]
            if len(s) > 30:
                # 滚动 60 日分位 -> 0..1
                rolling_rank = s.rolling(60, min_periods=20).apply(
                    lambda x: (x <= x.iloc[-1]).mean() if len(x) else 0.5, raw=False)
                series = rolling_rank.clip(0.0, 1.0).fillna(0.5)
    except Exception as exc:  # noqa: BLE001
        logger.debug("北向资金加载失败（将回退中性）：%s", exc)

    if series is not None and len(series) > 0:
        cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            import pickle
            with open(cache_path, "wb") as f:
                pickle.dump(series, f)
        except Exception:
            pass
        return series
    return None
