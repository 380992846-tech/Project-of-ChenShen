"""
config/settings.py
==================

统一配置管理入口。

设计要点
--------
- 使用 ``pydantic-settings`` 加载 ``config.yaml``，并把关键路径、市场、风控、
  数据源、API 等暴露为类型安全的属性。
- 支持环境变量 ``QUANT_`` 前缀覆盖（如 ``QUANT_ENVIRONMENT=live``）。
- 在纯离线环境下也能工作：不依赖 akshare/sklearn 等重型包。

用法
----
    from 量化系统.config import get_settings
    settings = get_settings()
    print(settings.market.sector)   # -> "TMT"
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（本文件所在目录的上级，即 量化系统/）
PKG_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


# --------------------------------------------------------------------------
# 数据模型（与 config.yaml 对应）
# --------------------------------------------------------------------------
class MarketConfig(BaseModel):
    region: str = "CN"
    sector: str = "TMT"
    benchmark: str = "510300"
    start_date: str = "2018-01-01"
    end_date: str = "2026-12-31"


class CostConfig(BaseModel):
    commission: float = 0.00015
    slippage: float = 0.0005
    stamp_tax: float = 0.0005


class BacktestConfig(BaseModel):
    initial_capital: float = 1_000_000
    risk_free_rate: float = 0.02
    cost: CostConfig = Field(default_factory=CostConfig)
    rebalance_freq: str = "daily"
    synthetic_annual_vol: float = 0.30
    synthetic_seed: int = 2024


class ParamScanConfig(BaseModel):
    enabled: bool = False
    momentum_window: list[int] = [10, 20, 30]
    top_n: list[int] = [2, 3, 4]


class StrategyConfig(BaseModel):
    name: str = "tmt_rotation"
    momentum_window: int = 40
    trend_window: int = 120
    top_n: int = 3
    fund_flow_weight: float = 0.0
    param_scan: ParamScanConfig = Field(default_factory=ParamScanConfig)


class RiskConfig(BaseModel):
    max_position: float = 0.95
    target_vol: float = 0.12
    vol_cap: float = 0.25
    stop_loss: float = 0.07
    take_profit: float = 0.15
    max_hold_days: int = 30
    max_drawdown_halt: float = 0.15
    per_name_limit: float = 0.40
    # 事中实时风控（InTradeRisk）
    vol_lookback: int = 20
    vol_floor: float = 0.20
    halt_scale: float = 0.5
    recover_ratio: float = 0.7


class SyntheticConfig(BaseModel):
    base_price: float = 100
    annual_vol: float = 0.30
    seed: int = 2024


class DataConfig(BaseModel):
    cache_dir: str = "data_cache"
    sources_priority: list[str] = ["synthetic"]
    synthetic: SyntheticConfig = Field(default_factory=SyntheticConfig)


class StorageConfig(BaseModel):
    sqlite_path: str = "quant.db"
    snapshot_dir: str = "snapshots"


class SchedulerConfig(BaseModel):
    enabled: bool = False
    data_update: str = "30 15 * * 1-5"
    signal_generation: str = "40 15 * * 1-5"
    daily_report: str = "50 15 * * 1-5"


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    poll_interval: int = 30


class LLMConfig(BaseModel):
    enabled: bool = False
    endpoint: str = "https://api.openai.com"
    api_key: str = ""
    model: str = "gpt-4o-mini"


class Settings(BaseSettings):
    """整个量化系统的顶层配置。"""

    model_config = SettingsConfigDict(
        env_prefix="QUANT_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: Literal["offline", "paper", "live"] = "offline"
    universe_source: Literal["curated", "akshare"] = "curated"
    market: MarketConfig = Field(default_factory=MarketConfig)
    universe: dict[str, dict[str, list[str]]] = Field(default_factory=dict)
    backtest: BacktestConfig = Field(default_factory=BacktestConfig)
    strategy: StrategyConfig = Field(default_factory=StrategyConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)

    @field_validator("universe")
    @classmethod
    def _ensure_universe(cls, v: dict) -> dict:
        if not v:
            v = {
                "groups": {
                    "半导体": ["512480", "159995"],
                    "软件服务": ["515230", "159852"],
                    "消费电子": ["159732", "515980"],
                    "通信设备": ["515880", "159869"],
                    "传媒游戏": ["512980", "516160"],
                }
            }
        return v

    # --- 便捷路径 ---
    @property
    def cache_dir(self) -> Path:
        p = Path(self.data.cache_dir)
        return p if p.is_absolute() else PKG_ROOT / p

    @property
    def sqlite_path(self) -> Path:
        p = Path(self.storage.sqlite_path)
        return p if p.is_absolute() else PKG_ROOT / p

    @property
    def snapshot_dir(self) -> Path:
        p = Path(self.storage.snapshot_dir)
        return p if p.is_absolute() else PKG_ROOT / p

    @property
    def universe_groups(self) -> dict[str, list[str]]:
        """返回 TMT 标的池（group -> symbols）。

        ``universe_source=curated``：直接用 config 里的真实成分股。
        ``universe_source=akshare``：联网拉取真实行业成分（失败回退内置真实成分股）。
        """
        if self.universe_source == "curated":
            return self.universe.get("groups", {})
        try:
            from 量化系统.data.universe import get_universe
            dyn = get_universe(self)
            if dyn:
                return dyn
        except Exception:
            pass
        return self.universe.get("groups", {})

    @property
    def universe_flat(self) -> dict[str, str]:
        """把 universe.groups 展平为 symbol -> group 的映射，便于按行业分组。"""
        flat: dict[str, str] = {}
        for group, symbols in self.universe_groups.items():
            for sym in symbols:
                flat.setdefault(str(sym), group)
        return flat

    @property
    def universe_symbols(self) -> list[str]:
        return list(self.universe_flat.keys())


# --------------------------------------------------------------------------
# 单例
# --------------------------------------------------------------------------
_settings: Settings | None = None


def _load_yaml() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def _apply_env_overrides(data: dict) -> dict:
    """把 ``QUANT_`` 前缀的环境变量叠加到 YAML 字典上（env 优先）。

    pydantic-settings 的 env 会被初始化 kwargs 覆盖，因此这里手动合并：
    ``QUANT_LLM__ENABLED=true`` -> data['llm']['enabled']=True。
    支持嵌套（用 ``__`` 分隔）与原生 YAML 的标量/字符串覆盖。
    """
    import os as _os

    for key, val in _os.environ.items():
        if not key.startswith("QUANT_"):
            continue
        rel = key[len("QUANT_"):]
        # 环境变量名通常大写；模型字段是小写，故统一小写处理
        parts = [p.lower() for p in rel.split("__")]
        nested = data
        for p in parts[:-1]:
            child = nested.setdefault(p, {})
            if not isinstance(child, dict):
                child = {}
                nested[p] = child
            nested = child
        # 布尔/数字字符串转原生类型
        val_str = val.strip()
        if val_str.lower() in ("true", "false"):
            val = val_str.lower() == "true"
        elif val_str.replace(".", "", 1).isdigit():
            val = float(val_str) if "." in val_str else int(val_str)
        nested[parts[-1]] = val
    return data


def get_settings(overrides: dict | None = None) -> Settings:
    """返回（并缓存）配置单例。

    加载顺序（低 -> 高）：config.yaml < QUANT_ 环境变量 < 显式 ``overrides``。
    """
    global _settings
    if _settings is None:
        raw = _load_yaml() or {}
        raw = _apply_env_overrides(raw)
        _settings = Settings(**raw)
    if overrides:
        merged = _settings.model_dump()
        merged.update(overrides)
        _settings = Settings(**merged)
    return _settings


def reset_settings() -> None:
    """测试/重载用：清空单例缓存。"""
    global _settings
    _settings = None
