"""
data/universe.py
================

TMT 板块真实标的池（成分股）。

设计目标
--------
- 提供「子行业分组 -> 成分股列表」的 TMT 标的池，并给出 ``symbol -> industry`` 映射。
- 默认使用**真实 A股 TMT 成分股**（按 THS 行业/概念板块整理，覆盖
  半导体 / 软件服务 / 消费电子 / 通信设备 / 传媒游戏）。
- 支持 :meth:`fetch_akshare_universe` 尝试用 akshare 自动拉取行业成分（尽力而为）；
  失败或离线时自动回退到内置的 :data:`CURATED_UNIVERSE` 真实成分股列表。
- 提供缓存（``universe_cache.json``），避免每次启动重复联网。

说明
----
- 内置成分股均为**真实、流动性较好的 A股**，按 THS 行业板块归类；代码无需带交易所前缀，
  由数据源自动识别（存在 sh/sz 前缀由 Sina/东财逻辑决定）。
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from 量化系统.config import get_settings

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# 内置真实 TMT 成分股（按子行业分组）
# --------------------------------------------------------------------------
CURATED_UNIVERSE: dict[str, list[str]] = {
    "半导体": ["688981", "603501", "688012", "002049", "688536", "300661", "603986", "688008"],
    "软件服务": ["600588", "002230", "688111", "300454", "002410", "600845", "688095", "603019"],
    "消费电子": ["002475", "002241", "600745", "000100", "601138", "300433", "002600", "300207"],
    "通信设备": ["000063", "600941", "300308", "002396", "601728", "600522", "300394", "000988"],
    "传媒游戏": ["002624", "002555", "002027", "300315", "603444", "300002", "002174", "600977"],
}

# 每个子行业的展示名称（用于中台“行业配置”标签）
GROUP_LABELS: dict[str, str] = {
    "半导体": "半导体",
    "软件服务": "软件服务",
    "消费电子": "消费电子",
    "通信设备": "通信设备",
    "传媒游戏": "传媒游戏",
}


def _cache_path(settings: Any) -> Path:
    digest = hashlib.sha1(str(settings.universe).encode("utf-8")).hexdigest()[:8]
    return settings.cache_dir / f"universe_{digest}.json"


def _normalize_universe(groups: dict[str, list[str]]) -> dict[str, list[str]]:
    """去重并剔除明显非 6 位代码的脏数据。"""
    out: dict[str, list[str]] = {}
    for group, syms in groups.items():
        seen: list[str] = []
        for s in syms:
            s = str(s).strip()
            if len(s) == 6 and s.isdigit() and s not in seen:
                seen.append(s)
        out[group] = seen
    return out


def fetch_akshare_universe(settings: Any = None) -> dict[str, list[str]] | None:
    """尽力用 akshare 拉取真实行业成分（基于东财行业板块）。

    当前东财板块成分接口在部分网络环境不稳定（502/断连），因此这里的联网拉取
    是**尽力而为**：任一接口不可用即返回 None，由调用方回落内置成分股。
    """
    settings = settings or get_settings()
    try:
        import akshare as ak
    except Exception:
        return None
    try:
        # 行业板块名称表（代码）
        names = ak.stock_board_industry_name_em()
        names.columns = [str(c) for c in names.columns]
        name_col = next((c for c in names.columns if "名称" in c), None)
        if name_col is None:
            return None
        board_names = names[name_col].tolist()

        TMT_KEYWORDS = ["半导体", "软件", "电子", "通信", "传媒", "游戏",
                        "计算机", "互联网", "光学", "元件", "IT服务", "消费电子"]
        wanted = [n for n in board_names if any(k in str(n) for k in TMT_KEYWORDS)]
        if not wanted:
            return None

        groups: dict[str, list[str]] = {}
        for name in wanted[:6]:  # 限制数量避免过度请求
            try:
                cons = ak.stock_board_industry_cons_em(symbol=name)
                cons.columns = [str(c) for c in cons.columns]
                code_col = next((c for c in cons.columns if "代码" in c), None)
                if code_col is None:
                    continue
                codes = [str(x) for x in cons[code_col].tolist() if len(str(x)) == 6]
                if codes:
                    groups[str(name)] = codes[:12]
            except Exception as exc:  # noqa: BLE001
                logger.warning("行业 %s 成分拉取失败：%s", name, exc)
        return _normalize_universe(groups) if groups else None
    except Exception as exc:  # noqa: BLE001
        logger.warning("akshare 标的池拉取失败：%s", exc)
        return None


def get_universe(settings: Any = None, use_akshare: bool = True) -> dict[str, list[str]]:
    """返回 TMT 标的池（group -> symbols）。

    优先级：akshare 拉取（若可用并缓存） -> 内置真实成分股。
    """
    settings = settings or get_settings()
    cache = _cache_path(settings)

    # 尝试联网拉取并缓存
    if use_akshare:
        try:
            if cache.exists():
                with open(cache, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if cached:
                    return _normalize_universe(cached)
            fetched = fetch_akshare_universe(settings)
            if fetched:
                cache.parent.mkdir(parents=True, exist_ok=True)
                with open(cache, "w", encoding="utf-8") as f:
                    json.dump(fetched, f, ensure_ascii=False, indent=2)
                return fetched
        except Exception as exc:  # noqa: BLE001
            logger.warning("联网拉取标的池失败，使用内置：%s", exc)

    # 回退：内置真实成分股
    return _normalize_universe(CURATED_UNIVERSE)


def build_universe_flat(settings: Any = None, use_akshare: bool = True) -> dict[str, str]:
    """返回 ``symbol -> industry`` 扁平映射（去重；多所属取第一个）。"""
    groups = get_universe(settings, use_akshare)
    flat: dict[str, str] = {}
    for group, syms in groups.items():
        for s in syms:
            flat.setdefault(s, group)
    return flat


def build_universe_symbols(settings: Any = None, use_akshare: bool = True) -> list[str]:
    return list(build_universe_flat(settings, use_akshare).keys())
