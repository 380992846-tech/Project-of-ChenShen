"""
service/orchestrator.py
=======================

量化系统编排器：把「数据 -> 策略 -> 风控 -> 回测 -> 持久化 -> 中台状态」串成一条流水。

对外核心接口
------------
- :meth:`QuantService.run` —— 执行一次完整流水，返回 DashboardState。
- :meth:`QuantService.dashboard` —— 返回可直接给前端渲染的状态字典（JSON 友好）。
- 数据会**缓存**在内存，避免每次接口调用都重复拉取/训练。

这样的分层让「策略引擎」与「交易执行 / API / 前端」解耦，便于后续微服务化。
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from 量化系统.config import get_settings
from 量化系统.data.loader import build_panel, PricePanel
from 量化系统.strategy import build_strategy
from 量化系统.backtest.engine import run_backtest, run_benchmark
from 量化系统.backtest.report import (build_summary_payload, nav_curve_payload,
                                       allocation_payload, equity_curve_chart)
from 量化系统.risk import RiskManager
from 量化系统.service.logging_setup import get_logger
from 量化系统.service.persistence import SQLiteStore

logger = get_logger(__name__)


@dataclass
class DashboardState:
    """给前端/接口使用的可序列化状态。"""
    strategy: str = ""
    environment: str = ""
    updated_at: str = ""
    summary: dict[str, Any] = field(default_factory=dict)
    kpis: dict[str, Any] = field(default_factory=dict)
    nav_curve: list[dict[str, Any]] = field(default_factory=list)
    allocation: dict[str, float] = field(default_factory=dict)
    trades: list[dict[str, Any]] = field(default_factory=list)
    positions: list[dict[str, Any]] = field(default_factory=list)
    benchmark_nav: list[dict[str, Any]] = field(default_factory=list)
    signals: list[dict[str, Any]] = field(default_factory=list)
    chart_path: str | None = None
    latest_trades: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "environment": self.environment,
            "updated_at": self.updated_at,
            "summary": self.summary,
            "kpis": self.kpis,
            "nav_curve": self.nav_curve,
            "allocation": self.allocation,
            "trades": self.trades,
            "positions": self.positions,
            "benchmark_nav": self.benchmark_nav,
            "signals": self.signals,
            "chart_path": self.chart_path,
            "latest_trades": self.latest_trades,
        }


class QuantService:
    """编排器。单例使用，内部持有 panel / result / 锁。"""

    def __init__(self, settings: Any = None, run_id: int | None = None):
        self.settings = settings or get_settings()
        self.store = SQLiteStore(self.settings.sqlite_path)
        self._run_id = run_id
        self._panel: PricePanel | None = None
        self._result = None
        self._benchmark_nav: pd.Series | None = None
        self._strategy = None
        self.dashboard_state: DashboardState = DashboardState()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # 内部：加载数据（带缓存）
    # ------------------------------------------------------------------
    def _load_panel(self) -> PricePanel:
        if self._panel is not None:
            return self._panel
        symbols = self.settings.universe_symbols
        logger.info("加载标的 %s ...", symbols)
        self._panel = build_panel(symbols, settings=self.settings)
        logger.info("数据面板就绪：%d 标的，%d 天", len(self._panel.symbols), len(self._panel.close))
        return self._panel

    def _load_benchmark_close(self) -> pd.Series | None:
        """加载基准标的收盘价；失败则返回 None（无基准对比）。"""
        if getattr(self, "_benchmark_close", None) is not None:
            return self._benchmark_close
        from 量化系统.data.loader import load_market_data
        bm = self.settings.market.benchmark
        try:
            data = load_market_data([bm], settings=self.settings)
            if bm in data:
                self._benchmark_close = data[bm]["close"].dropna()
                return self._benchmark_close
        except Exception as exc:  # noqa: BLE001
            logger.warning("基准 %s 加载失败：%s", bm, exc)
        return None

    # ------------------------------------------------------------------
    # 主流水
    # ------------------------------------------------------------------
    def run(self, strategy_name: str | None = None, force: bool = False) -> DashboardState:
        with self._lock:
            strategy_name = strategy_name or self.settings.strategy.name
            panel = self._load_panel()

            # 策略
            strategy = build_strategy(strategy_name, self.settings)
            strategy.on_data(panel)
            weights = strategy.generate_signals(panel)

            # 事前风控
            risk = RiskManager(self.settings)
            weights = risk.pre_trade(weights, panel)

            # 事中实时风控：滚动波动率自适应仓位 + 回撤熔断/恢复（贯穿全程）
            weights = risk.in_trade(weights, panel=panel)

            # 回测（用风控后的权重）
            result = run_backtest(panel, strategy, target_weights=weights)

            # 基准（单独加载沪深300，若不在 TMT 标的池中）
            benchmark_close = self._load_benchmark_close()
            benchmark_nav = run_benchmark(panel, benchmark_close=benchmark_close)

            # 图表
            chart_path = equity_curve_chart(result, self.settings.snapshot_dir)

            self._result = result
            self._strategy = strategy
            self._benchmark_nav = benchmark_nav

            # 持久化
            run_id = self._record_run(result, strategy, benchmark_nav, weights)

            self.dashboard_state = self._build_state(result, strategy, benchmark_nav, chart_path)
            return self.dashboard_state

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------
    def _record_run(self, result, strategy, benchmark_nav, weights) -> int:
        env = self.settings.environment
        run_id = self.store.record_run(strategy.name, env, strategy.params)
        trades_payload = _trades_payload(result)
        self.store.record_trades(run_id, trades_payload)
        self.store.record_positions(run_id, weights)
        summary = build_summary_payload(result, benchmark_nav)
        self.store.record_snapshot(run_id, str(result.nav.index[-1].date()),
                                   summary.get("metrics", {}),
                                   float(benchmark_nav.iloc[-1]) if benchmark_nav is not None and len(benchmark_nav) else None)
        return run_id

    # ------------------------------------------------------------------
    # 构建中台状态
    # ------------------------------------------------------------------
    def _build_state(self, result, strategy, benchmark_nav, chart_path) -> DashboardState:
        summary = build_summary_payload(result, benchmark_nav)
        held = sum(1 for p in _positions_payload(result))
        buys = sum(1 for t in result.trades if t.get("action") == "buy") if result.trades else 0
        kpis = {
            "aum": float(result.nav.iloc[-1]),
            "active_trades": held,                     # 当前持仓数量
            "pending_signals": int(buys),              # 累计买入信号数
            "risk_level": _risk_level(summary.get("metrics", {})),
            "max_drawdown": summary.get("metrics", {}).get("max_drawdown", 0.0),
            "sharpe": summary.get("metrics", {}).get("sharpe", 0.0),
            "total_return": summary.get("metrics", {}).get("total_return", 0.0),
        }
        return DashboardState(
            strategy=strategy.name,
            environment=self.settings.environment,
            updated_at=pd.Timestamp.now().isoformat(timespec="seconds"),
            summary=summary,
            kpis=kpis,
            nav_curve=nav_curve_payload(result),
            allocation=allocation_payload(result),
            trades=_trades_payload(result)[-40:],
            positions=_positions_payload(result),
            benchmark_nav=_nav_payload(benchmark_nav),
            signals=_signals_payload(result),
            chart_path=chart_path,
            latest_trades=_trades_payload(result)[-8:],
        )

    # ------------------------------------------------------------------
    # 便捷接口
    # ------------------------------------------------------------------
    def dashboard(self) -> dict[str, Any]:
        self._ensure_run()
        return self.dashboard_state.to_dict()

    def backtest(self) -> dict[str, Any]:
        self._ensure_run()
        return self.dashboard_state.summary

    def portfolio(self) -> dict[str, Any]:
        self._ensure_run()
        return {
            "allocation": self.dashboard_state.allocation,
            "positions": self.dashboard_state.positions,
        }

    def signals(self) -> dict[str, Any]:
        self._ensure_run()
        return {"signals": self.dashboard_state.signals,
                "latest_trades": self.dashboard_state.latest_trades}

    def explain_symbol(self, symbol: str, action: str | None = None) -> dict[str, Any]:
        """为某只标的构建自然语言信号解释。

        从面板取该标的最新的因子值，配合策略可能给出的特征重要性（如 XGBoost/SHAP），
        交给 :class:`量化系统.service.explainer.Explainer` 生成解释。
        """
        self._ensure_run()
        from 量化系统.service.explainer import build_explainer

        if self._panel is None or symbol not in self._panel.close.columns:
            return {"symbol": symbol, "explanation": f"未找到标的 {symbol} 的数据。", "factors": []}

        latest = self._panel.close.index[-1]
        df = self._panel.per_symbol.get(symbol)
        # 取最近一个非 NaN 的特征值
        factor_values: dict[str, float] = {}
        if df is not None:
            for col in ["rsi", "momentum_20", "momentum_60", "ma_bias", "volatility",
                        "trend", "volume_ratio", "bb_position", "atr"]:
                if col in df.columns:
                    s = df[col].dropna()
                    if len(s):
                        factor_values[col] = float(s.iloc[-1])

        # 特征重要性：策略若保存了则用；否则用因子绝对值做权重近似
        feature_importance: dict[str, float] = {}
        strat = getattr(self, "_strategy", None)
        if strat is not None:
            fi = getattr(strat, "state", {}).get("feature_importance")
            if fi:
                feature_importance = {k: float(v) for k, v in fi.items()}
        if not feature_importance and factor_values:
            total = sum(abs(v) for v in factor_values.values()) or 1.0
            feature_importance = {k: abs(v) / total for k, v in factor_values.items()}

        # 最近一次该标的的交易动作作为缺省 action
        if action is None:
            for t in reversed(self._result.trades):
                if t.get("symbol") == symbol:
                    action = t.get("action", "buy")
                    break
            action = action or "buy"

        price = float(self._panel.close.loc[latest, symbol])
        explainer = build_explainer(feature_importance, factor_values)
        result = explainer.explain(symbol=symbol, action=action, price=price)
        result["asof"] = str(latest.date())
        return result

    def _ensure_run(self):
        if self._result is None:
            self.run()


# --------------------------------------------------------------------------
# 语义化：风险等级
# --------------------------------------------------------------------------
def _risk_level(metrics: dict[str, Any]) -> str:
    mdd = abs(float(metrics.get("max_drawdown", 0.0)))
    if mdd > 0.20:
        return "高"
    if mdd > 0.12:
        return "中"
    return "低"


# --------------------------------------------------------------------------
# 序列化辅助
# --------------------------------------------------------------------------
def _trades_payload(result) -> list[dict[str, Any]]:
    out = []
    for t in result.trades:
        out.append({
            "date": str(pd.Timestamp(t["date"]).date()) if t.get("date") is not None else "",
            "symbol": t.get("symbol", ""),
            "action": t.get("action", ""),
            "price": round(float(t.get("price", 0.0)), 4),
            "notional": round(float(t.get("notional", 0.0)), 2),
            "weight": round(float(t.get("weight", 0.0)), 4),
            "reason": t.get("reason", ""),
        })
    return out


def _positions_payload(result) -> list[dict[str, Any]]:
    pos = result.positions
    if len(pos) == 0:
        return []
    nonzero = (pos.abs().sum(axis=1) > 1e-9)
    last_label = pos.index[nonzero].max() if nonzero.any() else pos.index[-1]
    last = pos.loc[last_label]
    sym_group = get_settings().universe_flat
    out = []
    for sym, w in last.items():
        if abs(w) > 1e-6:
            out.append({
                "symbol": sym,
                "weight": round(float(w), 4),
                "industry": sym_group.get(sym, "其他"),
            })
    return out


def _signals_payload(result) -> list[dict[str, Any]]:
    """近似信号：最近一次买卖动作。"""
    out = []
    for t in result.trades[-20:]:
        out.append({
            "symbol": t.get("symbol", ""),
            "action": t.get("action", ""),
            "date": str(pd.Timestamp(t["date"]).date()) if t.get("date") is not None else "",
            "price": round(float(t.get("price", 0.0)), 4),
        })
    return out


def _nav_payload(nav: pd.Series, max_points: int = 200) -> list[dict[str, Any]]:
    if nav is None or len(nav) == 0:
        return []
    step = max(1, len(nav) // max_points)
    return [{"date": str(nav.index[i].date()), "nav": float(nav.iloc[i])}
            for i in range(0, len(nav), step)]
