"""backtest 包：回测引擎、绩效指标、报告生成。"""
from 量化系统.backtest.engine import BacktestResult, run_backtest, run_benchmark
from 量化系统.backtest.metrics import (
    summary_metrics,
    sharpe_ratio,
    max_drawdown,
    drawdown_series,
    annualized_return,
    total_return,
)
from 量化系统.backtest.report import (
    build_summary_payload,
    nav_curve_payload,
    allocation_payload,
    equity_curve_chart,
)

__all__ = [
    "BacktestResult",
    "run_backtest",
    "run_benchmark",
    "summary_metrics",
    "sharpe_ratio",
    "max_drawdown",
    "drawdown_series",
    "annualized_return",
    "total_return",
    "build_summary_payload",
    "nav_curve_payload",
    "allocation_payload",
    "equity_curve_chart",
]
