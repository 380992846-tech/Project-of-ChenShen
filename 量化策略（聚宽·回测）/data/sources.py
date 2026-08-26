"""
data/sources.py
================

多数据源抽象层：统一 ``fetch(symbol, start, end) -> pd.DataFrame`` 接口。

设计目标
--------
- 数据源可插拔，按配置 ``sources_priority`` 依次尝试，失败自动回退。
- 每条数据源输出统一 schema：``[date, open, high, low, close, volume]``，
  以 ``date`` 为索引。
- **离线兜底**：:class:`SyntheticSource` 用带可复现种子的随机过程生成确定性行情，
  确保系统在没有 akshare/yfinance/baostock、没有网络的场景下也能完整跑通。

已封装数据源
------------
- :class:`SyntheticSource` —— 确定性 GBM + 波动聚集（离线兜底）
- :class:`AKShareSource`  —— 免费 A 股数据（akshare，可选安装）
- :class:`YFinanceSource` —— 美股/ETF（yfinance，可选安装）
- :class:`BaostockSource` —— A 股历史（baostock，可选安装）
"""

from __future__ import annotations

import os
import pickle
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from 量化系统.config import get_settings


def _cache_path(symbol: str, cache_dir: Path) -> Path:
    safe = symbol.replace(".", "_").replace("/", "_")
    return cache_dir / f"{safe}.pkl"


def _normalize_columns(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """把任意数据源输出规范成标准列名，并以 date 为索引。"""
    df = df.copy()
    cols = {c.lower(): c for c in df.columns}
    rename = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    out = {}
    for k, v in rename.items():
        if k in cols:
            out[k] = df[cols[k]]
    if "close" not in out:
        raise ValueError(f"数据源未返回 close 列: {symbol}")
    if not out.get("open", None) is not None:
        out["open"] = out["close"]
    if not out.get("high", None) is not None:
        out["high"] = out["close"]
    if not out.get("low", None) is not None:
        out["low"] = out["close"]
    if not out.get("volume", None) is not None:
        out["volume"] = 0.0
    out = pd.DataFrame(out)
    # 若有一列日期，转成索引
    if "date" in cols:
        out.index = pd.to_datetime(df[cols["date"]])
    else:
        out.index = pd.to_datetime(out.index)
    out = out.sort_index()
    return out


# --------------------------------------------------------------------------
# 抽象基类
# --------------------------------------------------------------------------
class DataSource(ABC):
    name: str = "base"

    @abstractmethod
    def fetch(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """返回规范化行情 DataFrame。"""

    def __repr__(self) -> str:  # pragma: no cover - 展示用
        return f"<DataSource {self.name}>"


# --------------------------------------------------------------------------
# 离线合成数据源
# --------------------------------------------------------------------------
class SyntheticSource(DataSource):
    """用可复现随机过程生成 OHLCV，离线也能跑。

    使用 Geometric Brownian Motion 生成收盘价，并在收盘价基础上构造
    高/低/开（含日内波动），成交量与波动率有简单聚集效应。
    """

    name = "synthetic"

    def __init__(self, base_price: float = 100.0, annual_vol: float = 0.30, seed: int = 2024):
        self.base_price = base_price
        self.annual_vol = annual_vol
        self.seed = seed

    def fetch(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        # 每个 symbol 一个稳定的种子，保证重复运行结果一致
        seed = self.seed + sum(ord(c) for c in symbol)
        rng = np.random.default_rng(seed)
        dates = pd.bdate_range(start=start, end=end)
        if len(dates) < 2:
            dates = pd.bdate_range(start=start, end=end, periods=252)
        n = len(dates)
        dt = 1.0 / 252
        mu = 0.06  # 年化漂移
        sigma = self.annual_vol
        # GBM 收盘价
        shocks = rng.standard_normal(n) * sigma * np.sqrt(dt)
        log_ret = (mu - 0.5 * sigma**2) * dt + shocks
        close = self.base_price * np.exp(np.cumsum(log_ret))
        close = np.maximum(close, 0.1)
        # 日内构造：open=昨收，high/low 围绕 open/close 加一点波动
        open_ = np.concatenate([[close[0]], close[:-1]])
        intraday = sigma * np.sqrt(dt) * 0.5
        high = np.maximum(open_, close) * (1 + np.abs(rng.standard_normal(n)) * intraday)
        low = np.minimum(open_, close) * (1 - np.abs(rng.standard_normal(n)) * intraday)
        volume_base = 1_000_000
        volume = (volume_base * np.exp(rng.standard_normal(n) * 0.4)).astype(int)
        df = pd.DataFrame(
            {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
            index=dates,
        )
        return df


# --------------------------------------------------------------------------
# 可选的真实数据源（需要额外 pip 安装）
# --------------------------------------------------------------------------
class AKShareSource(DataSource):
    """akshare 免费 A 股/ETF 数据。依赖 ``akshare``。

    自动区分：
      - 股票（6/0/3 开头）：``stock_zh_a_hist``（东财）
      - ETF/基金（5/1/51/15 开头等）：优先 ``fund_etf_hist_em``，失败回退
        ``fund_etf_hist_sina``（新浪，更稳定）。这正是原项目采用的回落路径。
    """

    name = "akshare"

    @staticmethod
    def _is_etf(symbol: str) -> bool:
        code = symbol.split(".")[0]
        if len(code) != 6:
            return False
        return code.startswith(("5", "1", "15", "51", "56", "58")) or code.startswith(("159", "512", "515", "516", "511", "518", "588"))

    def fetch(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        import akshare as ak

        start_compact = start.replace("-", "")
        end_compact = end.replace("-", "")

        if self._is_etf(symbol):
            return self._fetch_etf(ak, symbol, start_compact, end_compact)

        # 优先东财（字段较全），西财在部分环境会被限流/断连，则回退新浪
        try:
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_compact,
                end_date=end_compact,
                adjust="qfq",
            )
            if df is not None and len(df) > 0:
                df.columns = [str(c) for c in df.columns]
                rename = {"日期": "date", "开盘": "open", "最高": "high",
                          "最低": "low", "收盘": "close", "成交量": "volume"}
                df = df.rename(columns=rename)
                return _normalize_columns(df, symbol)
        except Exception:
            pass
        # 新浪个股日线（可靠回退）
        return self._stock_sina_daily(ak, symbol, start_compact, end_compact)

    @staticmethod
    def _stock_sina_daily(ak, symbol: str, start_compact: str, end_compact: str) -> pd.DataFrame:
        """新浪个股日线（稳定，东财被限流/断连时的可靠回退）。

        代码需带交易所前缀：sh6… / sz0… / sz3…（科创板 sh688…）。
        """
        prefix = "sh" if symbol.startswith(("6", "68", "5")) else "sz"
        prefixed = f"{prefix}{symbol}"
        df = ak.stock_zh_a_daily(symbol=prefixed, start_date=start_compact,
                                 end_date=end_compact, adjust="qfq")
        if df is None or len(df) == 0:
            raise ValueError(f"akshare(新浪个股) 未返回数据: {symbol}")
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df[["date", "open", "high", "low", "close", "volume"]]
        return _normalize_columns(df, symbol)

    @staticmethod
    def _fetch_etf(ak, symbol: str, start_compact: str, end_compact: str) -> pd.DataFrame:
        # 尝试东财（字段较全，但当前可能连接不稳定）
        try:
            df = ak.fund_etf_hist_em(
                symbol=symbol, period="daily",
                start_date=start_compact, end_date=end_compact, adjust="qfq")
            if df is not None and len(df) > 0:
                df.columns = [str(c) for c in df.columns]
                rename = {"日期": "date", "开盘": "open", "最高": "high",
                          "最低": "low", "收盘": "close", "成交量": "volume"}
                df = df.rename(columns=rename)
                return _normalize_columns(df, symbol)
        except Exception:
            pass
        # 回退到新浪（更稳定的免费源），代码需带交易所前缀
        suffix = "sh" if symbol.startswith("5") else ("sz" if symbol.startswith("1") else "sh")
        prefixed = f"{suffix}{symbol}"
        df = ak.fund_etf_hist_sina(symbol=prefixed)
        if df is None or len(df) == 0:
            raise ValueError(f"akshare(新浪ETF) 未返回数据: {symbol}")
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df[["date", "open", "high", "low", "close", "volume"]]
        return _normalize_columns(df, symbol)


class YFinanceSource(DataSource):
    """yfinance 数据。依赖 ``yfinance``。"""

    name = "yfinance"

    def fetch(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        import yfinance as yf

        data = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
        if data is None or len(data) == 0:
            raise ValueError(f"yfinance 未返回数据: {symbol}")
        df = data.copy()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        df.columns = [str(c).lower() for c in df.columns]
        return _normalize_columns(df, symbol)


class BaostockSource(DataSource):
    """baostock A 股历史数据。依赖 ``baostock``。"""

    name = "baostock"

    def fetch(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        import baostock as bs

        bs.login()
        code = symbol
        rs = bs.query_history_k_data_plus(
            code,
            "date,open,high,low,close,volume",
            start_date=start,
            end_date=end,
            frequency="d",
            adjustflag="2",
        )
        rows = []
        while rs.error_code == "0" and rs.next():
            rows.append(rs.get_row_data())
        bs.logout()
        if not rows:
            raise ValueError(f"baostock 未返回数据: {symbol}")
        df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume"])
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        return _normalize_columns(df, symbol)


# --------------------------------------------------------------------------
# 数据源工厂
# --------------------------------------------------------------------------
_SOURCE_CLASSES: dict[str, type[DataSource]] = {
    "synthetic": SyntheticSource,
    "akshare": AKShareSource,
    "yfinance": YFinanceSource,
    "baostock": BaostockSource,
}


def build_source(name: str, settings: Any = None) -> DataSource:
    """按名称构造数据源实例。"""
    settings = settings or get_settings()
    cls = _SOURCE_CLASSES.get(name)
    if cls is None:
        raise ValueError(f"未知数据源: {name}")
    if name == "synthetic":
        syn = settings.data.synthetic
        return SyntheticSource(base_price=syn.base_price, annual_vol=syn.annual_vol, seed=syn.seed)
    return cls()


def fetch_with_fallback(
    symbol: str,
    start: str,
    end: str,
    sources_priority: list[str] | None = None,
    settings: Any = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """按优先级尝试多个数据源，成功即返回（并写缓存）；全部失败抛错。"""
    settings = settings or get_settings()
    priority = sources_priority or settings.data.sources_priority
    cache_dir = settings.cache_dir

    if use_cache:
        path = _cache_path(symbol, cache_dir)
        if path.exists():
            try:
                with open(path, "rb") as f:
                    cached = pickle.load(f)
                if len(cached) > 0:
                    return cached
            except Exception:
                pass

    os.makedirs(cache_dir, exist_ok=True)
    last_err: Exception | None = None
    for name in priority:
        try:
            src = build_source(name, settings)
            df = src.fetch(symbol, start, end)
            df = _normalize_columns(df, symbol)
            if len(df) == 0:
                raise ValueError(f"{name} 返回空数据: {symbol}")
            if use_cache:
                with open(_cache_path(symbol, cache_dir), "wb") as f:
                    pickle.dump(df, f)
            return df
        except ModuleNotFoundError:
            # 该数据源未安装，跳过并继续
            last_err = ImportError(f"数据源 {name} 未安装")
            continue
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
    raise RuntimeError(f"所有数据源均失败: {symbol} ({last_err})")
