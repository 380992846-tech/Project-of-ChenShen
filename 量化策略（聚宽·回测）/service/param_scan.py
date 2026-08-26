"""
service/param_scan.py
=====================

策略参数扫描器。

设计要点
--------
- **单次加载行情面板**并复用，避免扫描大量参数组合时反复联网/读缓存。
- 对每个参数组合，走与 :meth:`量化系统.service.orchestrator.QuantService.run`
  相同的流水：策略 -> 事前风控 -> 回测 -> 绩效指标。
- 按目标函数（默认 夏普，可选 综合分）对所有组合排序，输出结果表与最优参数。
- 支持多策略对比与网格扫描。

用法
----
    from 量化系统.service.param_scan import scan_strategy_params
    best = scan_strategy_params("tmt_rotation", grid={"momentum_window":[10,20,30], "top_n":[2,3,4]})
"""

from __future__ import annotations

import itertools
from typing import Any, Callable

import numpy as np
import pandas as pd

from 量化系统.config import get_settings
from 量化系统.data.loader import build_panel, PricePanel
from 量化系统.strategy import build_strategy
from 量化系统.backtest.engine import run_backtest, run_benchmark
from 量化系统.risk import RiskManager
from 量化系统.service.logging_setup import get_logger

logger = get_logger(__name__)


def _objective(metrics: dict[str, float], weights: dict[str, float] | None = None) -> float:
    """综合目标函数（值越大越好）。

    默认按 夏普 排序；若提供 ``weights``，则用加权综合分。
    """
    if weights:
        score = 0.0
        for k, w in weights.items():
            v = metrics.get(k, 0.0)
            # 回撤为负，取绝对值越小越好 -> 用 (1 - |mdd|)
            if k == "max_drawdown":
                v = 1.0 - abs(v)
            score += w * v
        return float(score)
    return float(metrics.get("sharpe", 0.0))


def _run_one(panel: PricePanel, strategy_name: str, params: dict[str, Any], settings,
             risk: RiskManager, benchmark_close: pd.Series | None) -> dict[str, Any]:
    """对一组参数跑一次完整流水，返回结果指标。"""
    strategy = build_strategy(strategy_name, settings, **params)
    strategy.on_data(panel)
    weights = strategy.generate_signals(panel)
    weights = risk.pre_trade(weights, panel)
    # 与编排器一致：事中实时风控
    weights = risk.in_trade(weights, panel=panel)
    result = run_backtest(panel, strategy, target_weights=weights)
    benchmark_nav = run_benchmark(panel, benchmark_close=benchmark_close)
    return {
        "params": params,
        "metrics": result.metrics,
        "trades_count": len(result.trades),
        "result": result,
    }


def scan_strategy_params(
    strategy_name: str,
    grid: dict[str, list[Any]],
    settings: Any = None,
    sample_size: int | None = None,
    objective_weights: dict[str, float] | None = None,
    top_k: int = 10,
) -> dict[str, Any]:
    """对指定策略做参数网格扫描。

    参数
    ----
    strategy_name : 策略名。
    grid : {param: [候选值]}，做笛卡尔积。
    sample_size : 可选，仅用最后 N 个 bar（加速扫描）。
    objective_weights : 目标函数权重；缺省按夏普。
    top_k : 返回最优的前 k 个组合。

    返回
    ----
    dict：包含 ``results``(DataFrame) 与 ``best``(行)。
    """
    settings = settings or get_settings()
    panel = build_panel(settings.universe_symbols, settings=settings)
    if sample_size and sample_size > 0 and sample_size < len(panel.close):
        panel = _slice_panel(panel, sample_size)

    # 基准收盘价（沪深300，单独拉取一次）
    benchmark_close = _load_benchmark(settings)

    risk = RiskManager(settings)
    keys = list(grid.keys())
    values = list(grid.values())
    combos = list(itertools.product(*values))
    logger.info("网格 %s 组合：%s", len(combos), {k: len(v) for k, v in grid.items()})

    rows: list[dict[str, Any]] = []
    for combo in combos:
        params = dict(zip(keys, combo))
        try:
            res = _run_one(panel, strategy_name, params, settings, risk, benchmark_close)
        except Exception as exc:  # noqa: BLE001
            logger.warning("参数组合 %s 失败：%s", params, exc)
            continue
        m = res["metrics"]
        row = dict(params)
        row.update({f"m_{k}": round(v, 4) for k, v in m.items()})
        row["objective"] = round(_objective(m, objective_weights), 4)
        row["trades"] = res["trades_count"]
        row["_result"] = res["result"]
        rows.append(row)

    df = pd.DataFrame([{k: v for k, v in r.items() if k != "_result"} for r in rows])
    if df.empty:
        return {"results": df, "best": None, "objective_weights": objective_weights}
    df = df.sort_values("objective", ascending=False).reset_index(drop=True)

    best_row = rows[df.index[0]]
    return {
        "results": df,
        "best": {k: v for k, v in best_row.items() if k != "_result"},
        "best_result": best_row["_result"],
        "objective_weights": objective_weights,
    }


def _slice_panel(panel: PricePanel, n: int) -> PricePanel:
    """截取面板最后 n 行（用于快速扫描）。"""
    close = panel.close.tail(n)
    idx = close.index
    panel.close = close
    panel.open_ = panel.open_.reindex(idx)
    panel.high = panel.high.reindex(idx)
    panel.low = panel.low.reindex(idx)
    panel.volume = panel.volume.reindex(idx)
    panel.returns = panel.close.pct_change()
    panel.per_symbol = {s: df.reindex(idx).ffill() for s, df in panel.per_symbol.items()}
    return panel


def _load_benchmark(settings) -> pd.Series | None:
    from 量化系统.data.loader import load_market_data
    bm = settings.market.benchmark
    try:
        data = load_market_data([bm], settings=settings)
        if bm in data:
            return data[bm]["close"].dropna()
    except Exception as exc:  # noqa: BLE001
        logger.warning("基准 %s 加载失败：%s", bm, exc)
    return None


def _fold_oos_metrics(
    strategy_name: str,
    params: dict[str, Any],
    settings: Any,
    risk: RiskManager,
    oos_start: int,
    panel: PricePanel,
    benchmark_close: pd.Series | None,
    warmup: int = 60,
    oos_end: int | None = None,
) -> dict[str, float]:
    """只在 OOS 窗口 [oos_start, oos_end) 上评估一组参数。

    由于信号与风控都是因果（滚动窗口 + shift(1)），生成的权重轨迹在 OOS 段只依赖
    OOS 之前的过去数据，因此按时间切片即可得到**诚实的 out-of-sample** 指标。
    """
    strategy = build_strategy(strategy_name, settings, **params)
    strategy.on_data(panel)
    weights = strategy.generate_signals(panel)
    weights = risk.pre_trade(weights, panel)
    weights = risk.in_trade(weights, panel=panel)

    oos_panel = _window_panel(panel, oos_start, panel, oos_end)
    oos_weights = weights.loc[oos_panel.close.index]
    result = run_backtest(oos_panel, strategy, target_weights=oos_weights)
    return result.metrics


def _window_panel(panel: PricePanel, start: int, full: PricePanel,
                  end: int | None = None) -> PricePanel:
    """返回从 start 到 end（默认到结尾）的局部面板。

    说明：返回的面板只保留该窗口用于计算指标，但策略权重已在外部用完整
    面板（因果）算好，此处仅用于回测撮合对应窗口。
    """
    end = end if end is not None else len(panel.close)
    idx = panel.close.index[start:end]
    return PricePanel(
        settings=panel.settings,
        close=panel.close.loc[idx],
        open_=panel.open_.loc[idx],
        high=panel.high.loc[idx],
        low=panel.low.loc[idx],
        volume=panel.volume.loc[idx],
        returns=panel.returns.loc[idx],
        per_symbol={s: df.loc[idx] for s, df in panel.per_symbol.items()},
    )


def walk_forward_valid(
    strategy_name: str,
    grid: dict[str, list[Any]],
    n_folds: int = 4,
    settings: Any = None,
    in_sample_frac: float = 0.5,
    objective_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """滚动前推(out-of-sample)稳健性检验。

    流程
    ----
    1. 把时间轴切成 ``n_folds`` 个顺序折；每折的 **in-sample** 是前 ``in_sample_frac``
       比例，out-of-sample 是剩余部分（与 in-sample 不重叠，且在时间上靠后）。
    2. 每折在 in-sample 上用 ``grid`` 做小扫描，按目标函数选**本折最优参数**。
    3. 把该参数放到本折的 out-of-sample 段评估，得到 OOS 指标。
    4. 汇总：各折选出的参数一致性、OOS 平均夏普/收益/回撤、以及「固定当前默认参数
       的 OOS」作为对照，判断是否存在过拟合。

    返回
    ----
    dict：``folds``(每折明细)、``summary``(OOS 汇总)、``baseline``(固定默认参数的 OOS)。
    """
    settings = settings or get_settings()
    panel = build_panel(settings.universe_symbols, settings=settings)
    benchmark_close = _load_benchmark(settings)
    risk = RiskManager(settings)
    keys = list(grid.keys())
    values = list(grid.values())
    combos = list(itertools.product(*values))

    n = len(panel.close)
    val_size = max(n // (n_folds + 1), 40)  # 每个验证块的长度（至少 40 bar）
    warmup = 60
    baseline_params = {
        "momentum_window": settings.strategy.momentum_window,
        "trend_window": settings.strategy.trend_window,
        "top_n": settings.strategy.top_n,
    }

    folds = []
    for f in range(n_folds):
        # 验证块：时间段 [f*val_size, (f+1)*val_size)，in-sample 为该块之前的数据
        oos_start = f * val_size
        oos_end = min((f + 1) * val_size, n)
        if oos_end - oos_start < 40 or oos_start - warmup <= 0:
            continue
        in_start = 0
        in_end = oos_start
        if in_end - in_start < 40:
            continue

        # 在 in-sample 段做小扫描选最优
        in_params = None
        best_obj = -np.inf
        # in-sample 面板：只用 OOS 之前的全部历史（时间上严格靠前）
        in_panel = PricePanel(
            settings=panel.settings,
            close=panel.close.iloc[:in_end],
            open_=panel.open_.iloc[:in_end],
            high=panel.high.iloc[:in_end],
            low=panel.low.iloc[:in_end],
            volume=panel.volume.iloc[:in_end],
            returns=panel.returns.iloc[:in_end],
            per_symbol={s: df.iloc[:in_end] for s, df in panel.per_symbol.items()},
        )
        for combo in combos:
            params = dict(zip(keys, combo))
            m = _run_one(in_panel, strategy_name, params, settings, risk, benchmark_close)["metrics"]
            obj = _objective(m, objective_weights)
            if obj > best_obj:
                best_obj = obj
                in_params = params

        # OOS 评估（用选定参数；OOS 块 = [oos_start, oos_end)）
        oos_metrics = _fold_oos_metrics(strategy_name, in_params, settings, risk,
                                        oos_start, panel, benchmark_close, warmup, oos_end)
        folds.append({
            "fold": f,
            "in_params": in_params,
            "in_sharpe": best_obj,
            "oos_sharpe": round(oos_metrics.get("sharpe", 0.0), 4),
            "oos_total_return": round(oos_metrics.get("total_return", 0.0), 4),
            "oos_max_drawdown": round(oos_metrics.get("max_drawdown", 0.0), 4),
        })

    folds_df = pd.DataFrame(folds) if folds else pd.DataFrame()
    summary = {}
    if not folds_df.empty:
        summary = {
            "n_folds": int(len(folds_df)),
            "mean_oos_sharpe": round(float(folds_df["oos_sharpe"].mean()), 4),
            "mean_oos_total_return": round(float(folds_df["oos_total_return"].mean()), 4),
            "mean_oos_max_drawdown": round(float(folds_df["oos_max_drawdown"].mean()), 4),
            "best_sharpe_fold": int(folds_df.loc[folds_df["oos_sharpe"].idxmax(), "fold"])
            if len(folds_df) else None,
            "worst_sharpe_fold": int(folds_df.loc[folds_df["oos_sharpe"].idxmin(), "fold"])
            if len(folds_df) else None,
        }
        # 每折选出的参数是否一致
        in_params_list = [str(fl["in_params"]) for fl in folds]
        summary["param_consistency"] = round(
            (pd.Series(in_params_list).value_counts(normalize=True).max() or 0.0), 4)

    # 基线：固定当前默认参数的 OOS（作为对照，判断调优是否真优于默认）
    baseline = {}
    for f in range(n_folds):
        oos_start = f * val_size
        oos_end = min((f + 1) * val_size, n)
        if oos_end - oos_start < 40 or oos_start - warmup <= 0:
            continue
        m = _fold_oos_metrics(strategy_name, baseline_params, settings, risk,
                              oos_start, panel, benchmark_close, warmup, oos_end)
        baseline[f"fold_{f}"] = {
            "oos_sharpe": round(m.get("sharpe", 0.0), 4),
            "oos_total_return": round(m.get("total_return", 0.0), 4),
            "oos_max_drawdown": round(m.get("max_drawdown", 0.0), 4),
        }
    if baseline:
        bdf = pd.DataFrame(baseline).T
        baseline = {
            "mean_oos_sharpe": round(float(bdf["oos_sharpe"].mean()), 4),
            "mean_oos_total_return": round(float(bdf["oos_total_return"].mean()), 4),
            "mean_oos_max_drawdown": round(float(bdf["oos_max_drawdown"].mean()), 4),
        }

    return {"folds": folds_df, "summary": summary, "baseline": baseline}
