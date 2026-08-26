"""
backtest/report.py
==================

回测报告：生成图表（净值/回撤/持仓）并把绩效摘要转成结构化数据供 API 使用。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from 量化系统.config import get_settings
from 量化系统.backtest.engine import BacktestResult


def build_summary_payload(result: BacktestResult, benchmark_nav: pd.Series | None = None) -> dict:
    """构建用于前端/接口的绩效摘要（JSON 友好）。"""
    m = result.metrics
    bench = None
    if benchmark_nav is not None:
        from 量化系统.backtest.metrics import (
            total_return as _tr,
            sharpe_ratio as _sr,
            max_drawdown as _mdd,
        )
        bench = {
            "total_return": float(_tr(benchmark_nav)),
            "sharpe": float(_sr(benchmark_nav)),
            "max_drawdown": float(_mdd(benchmark_nav)),
        }
    return {
        "initial_capital": float(result.initial_capital),
        "final_nav": float(result.nav.iloc[-1]),
        "strategy": result.strategy_name,
        "metrics": {k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in m.items()},
        "benchmark": bench,
    }


def nav_curve_payload(result: BacktestResult, max_points: int = 800) -> list[dict]:
    """净值/回撤曲线数据（降采样）。"""
    nav = result.nav
    dd = result.drawdown
    n = len(nav)
    step = max(1, n // max_points)
    idx = range(0, n, step)
    return [
        {
            "date": str(nav.index[i].date()),
            "nav": float(nav.iloc[i]),
            "drawdown": float(dd.iloc[i] * 100),
        }
        for i in idx
    ]


def allocation_payload(result: BacktestResult) -> dict:
    """最终持仓的行业配置（按 universe 分组），供前端「资产配置」展示。

    使用**最近一个仍有持仓的 bar**（而非孤立的最后一个 bar），避免刚好平仓后显示为空。
    """
    settings = get_settings()
    pos = result.positions
    if len(pos) == 0:
        return {}
    # 找到最近一个出现非零权重的时间点
    nonzero_mask = (pos.abs().sum(axis=1) > 1e-9)
    last_label = pos.index[nonzero_mask].max() if nonzero_mask.any() else pos.index[-1]
    last_pos = pos.loc[last_label]
    sym_group = settings.universe_flat
    groups: dict[str, float] = {}
    for sym, weight in last_pos.items():
        if weight > 1e-6:
            g = sym_group.get(sym, "其他")
            groups[g] = groups.get(g, 0.0) + float(weight)
    return {k: round(v, 4) for k, v in sorted(groups.items(), key=lambda x: -x[1])}


def equity_curve_chart(result: BacktestResult, out_dir: Path | None = None) -> str | None:
    """用 matplotlib 画四联图（净值/回撤/持仓/收益分布），可保存。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    # 尝试选用一款支持中文的字体，避免方框/占位符
    for family in ("Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", "WenQuanYi Zen Hei"):
        try:
            if any(family.lower() in f.name.lower() for f in font_manager.fontManager.ttflist):
                plt.rcParams["font.sans-serif"] = [family]
                plt.rcParams["axes.unicode_minus"] = False
                break
        except Exception:
            continue

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    nav = result.nav
    axes[0, 0].plot(nav.index, nav.values, linewidth=1.4, color="#4f46e5")
    axes[0, 0].set_title("净值曲线")
    axes[0, 0].grid(alpha=0.3)

    dd = result.drawdown * 100
    axes[0, 1].fill_between(dd.index, 0, dd.values, color="#e07a8a", alpha=0.4)
    axes[0, 1].set_title("回撤(%)")
    axes[0, 1].grid(alpha=0.3)

    positions = result.positions
    for col in positions.columns[:6]:
        axes[1, 0].plot(positions.index, positions[col], label=str(col), linewidth=1.0)
    axes[1, 0].set_title("持仓权重")
    axes[1, 0].legend(fontsize=7)
    axes[1, 0].grid(alpha=0.3)

    r = result.returns
    axes[1, 1].hist(r.dropna(), bins=60, color="#7bc9b0", alpha=0.7)
    axes[1, 1].set_title("日收益分布")
    axes[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    path = None
    if out_dir is not None:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "equity_curve.png"
        fig.savefig(path, dpi=120)
    plt.close(fig)
    return str(path) if path else None
