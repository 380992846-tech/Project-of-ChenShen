"""
main.py —— TMT 量化系统入口。

用法
----
    python -m 量化系统.main run               # 跑一次完整流水（回测 + 持久化 + 图表）
    python -m 量化系统.main serve             # 启动 FastAPI 中台（默认 0.0.0.0:8000）
    python -m 量化系统.main dashboard --json   # 打印中台状态 JSON
    python -m 量化系统.main list-strategies    # 列出可用策略
    python -m 量化系统.main scan               # 参数扫描（--strategy/--grid/--sample）
    python -m 量化系统.main walk-forward        # 滚动前推 OOS 稳健性检验
"""

from __future__ import annotations

import argparse
import json
import sys

from 量化系统.config import get_settings
from 量化系统.service.logging_setup import get_logger
from 量化系统.strategy import STRATEGIES

logger = get_logger(__name__)


def run_pipeline(strategy_name: str | None = None) -> None:
    """执行一次完整流水。"""
    from 量化系统.service.orchestrator import QuantService

    settings = get_settings()
    svc = QuantService(settings)
    state = svc.run(strategy_name=strategy_name)
    logger.info("策略=%s 环境=%s", state.strategy, state.environment)
    logger.info("指标=%s", state.summary.get("metrics"))
    logger.info("行业配置=%s", state.allocation)
    logger.info("净值图=%s", state.chart_path)


def print_dashboard() -> None:
    from 量化系统.service.orchestrator import QuantService

    svc = QuantService(get_settings())
    print(json.dumps(svc.dashboard(), ensure_ascii=False, indent=2))


def serve() -> None:
    import uvicorn

    settings = get_settings()
    from 量化系统.api.server import app

    host, port = settings.api.host, settings.api.port
    logger.info("启动量化中台: http://%s:%s", host, port)
    uvicorn.run(app, host=host, port=port, log_level="info")


def list_strategies() -> None:
    for name, cls in STRATEGIES.items():
        print(f"{name:20s} {cls.__name__}")


def scan_params(strategy: str, grid_json: str | None = None, sample_size: int | None = None) -> None:
    """对指定策略做参数网格扫描，打印前 N 个组合。"""
    from 量化系统.service.param_scan import scan_strategy_params

    grid = {
        "momentum_window": [15, 20, 30, 45],
        "trend_window": [60, 120],
        "top_n": [2, 3, 4],
        "max_position": [0.7, 0.95],
    }
    if grid_json:
        import json as _json
        grid = _json.loads(grid_json)
    res = scan_strategy_params(
        strategy, grid, sample_size=sample_size, top_k=12)
    df = res["results"]
    if df is None or df.empty:
        print("无有效结果")
        return
    print(f"=== 参数扫描结果 {strategy} (组合 {len(df)}) ===")
    keys = list(grid.keys())
    cols = keys + ["m_sharpe", "m_total_return", "m_max_drawdown", "objective", "trades"]
    cols = [c for c in cols if c in df.columns]
    print(df[cols].head(15).to_string(index=False))
    print("--- BEST ---")
    if res.get("best"):
        print(res["best"])


def walk_forward(strategy: str, grid_json: str | None = None, n_folds: int = 5) -> None:
    """对指定策略做滚动前推 OOS 稳健性检验。"""
    from 量化系统.service.param_scan import walk_forward_valid

    grid = {"momentum_window": [30, 40, 60], "trend_window": [120], "top_n": [2, 3]}
    if grid_json:
        import json as _json
        grid = _json.loads(grid_json)
    res = walk_forward_valid(strategy, grid, n_folds=n_folds)
    print("=== FOLDS ===")
    if res["folds"] is not None and not res["folds"].empty:
        print(res["folds"].to_string(index=False))
    print("=== SUMMARY ===")
    print(res.get("summary"))
    print("=== BASELINE (默认参数) ===")
    print(res.get("baseline"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="TMT 量化系统")
    parser.add_argument("cmd", choices=["run", "serve", "dashboard", "list-strategies", "scan",
                                        "walk-forward"],
                        help="命令")
    parser.add_argument("--strategy", default=None, help="策略名（默认为配置）")
    parser.add_argument("--json", action="store_true", help="dashboard 输出为 JSON")
    parser.add_argument("--grid", default=None, help="扫描参数网格（JSON 字符串）")
    parser.add_argument("--sample", type=int, default=None, help="扫描用最后 N 个交易日")
    parser.add_argument("--n-folds", type=int, default=5, help="WFO 折数")
    args = parser.parse_args(argv)

    if args.cmd == "run":
        run_pipeline(args.strategy)
    elif args.cmd == "serve":
        serve()
    elif args.cmd == "dashboard":
        print_dashboard()
    elif args.cmd == "list-strategies":
        list_strategies()
    elif args.cmd == "scan":
        scan_params(args.strategy or "tmt_rotation", args.grid, args.sample)
    elif args.cmd == "walk-forward":
        walk_forward(args.strategy or "tmt_rotation", args.grid, args.n_folds)
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
