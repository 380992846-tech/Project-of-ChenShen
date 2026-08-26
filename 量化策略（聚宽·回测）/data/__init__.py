"""data 包：数据获取、清洗、缓存、因子计算、标的池。"""
from 量化系统.data.factors import (
    FACTORS,
    FACTOR_MAP,
    Factor,
    compute_factor,
    compute_factors,
    add_labels,
    clean_array,
    register_factor,
)
from 量化系统.data.loader import PricePanel, build_panel, load_market_data
from 量化系统.data.sources import (
    DataSource,
    SyntheticSource,
    fetch_with_fallback,
)
from 量化系统.data.universe import (
    CURATED_UNIVERSE,
    get_universe,
    build_universe_flat,
    build_universe_symbols,
)

__all__ = [
    "FACTORS",
    "FACTOR_MAP",
    "Factor",
    "compute_factor",
    "compute_factors",
    "add_labels",
    "clean_array",
    "register_factor",
    "PricePanel",
    "build_panel",
    "load_market_data",
    "DataSource",
    "SyntheticSource",
    "fetch_with_fallback",
    "CURATED_UNIVERSE",
    "get_universe",
    "build_universe_flat",
    "build_universe_symbols",
]
