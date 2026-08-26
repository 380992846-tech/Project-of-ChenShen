"""
service/persistence.py
======================

轻量持久化：用标准库 SQLite 保存每日持仓、交易记录、绩效快照，便于复盘。

- 不依赖重型 ORM；直接 sqlite3。
- 表：trades（逐笔）、positions（每日持仓）、snapshots（每日绩效）、runs（每次回测运行）。
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from 量化系统.config import get_settings

_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT,
    strategy TEXT,
    environment TEXT,
    params TEXT
);
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    date TEXT,
    symbol TEXT,
    side TEXT,
    price REAL,
    notional REAL,
    weight REAL,
    reason TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    date TEXT,
    symbol TEXT,
    weight REAL,
    industry TEXT
);
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    date TEXT,
    nav REAL,
    total_return REAL,
    annual_return REAL,
    sharpe REAL,
    max_drawdown REAL,
    benchmark_nav REAL
);
"""


class SQLiteStore:
    def __init__(self, path: Path | str | None = None):
        settings = get_settings()
        self.path = Path(path or settings.sqlite_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None  # 延迟连接，线程安全用单连接 + 锁
        self._init_schema()

    def _conn_ensure(self):
        import sqlite3
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        return self._conn

    def _init_schema(self):
        conn = self._conn_ensure()
        conn.executescript(_SCHEMA)
        conn.commit()

    # ---- runs ----
    def record_run(self, strategy: str, environment: str, params: dict[str, Any] | None = None) -> int:
        conn = self._conn_ensure()
        cur = conn.execute(
            "INSERT INTO runs(started_at, strategy, environment, params) VALUES (?,?,?,?)",
            (datetime.now().isoformat(timespec="seconds"), strategy, environment,
             json.dumps(params or {}, ensure_ascii=False)),
        )
        conn.commit()
        return int(cur.lastrowid)

    # ---- trades ----
    def record_trades(self, run_id: int, trades: Iterable[dict[str, Any]]) -> None:
        conn = self._conn_ensure()
        rows = [
            (
                run_id,
                str(t.get("date", "")),
                t.get("symbol", ""),
                t.get("action", "buy"),
                float(t.get("price", 0.0)),
                float(t.get("notional", 0.0)),
                float(t.get("weight", 0.0)),
                t.get("reason", None),
            )
            for t in trades
        ]
        conn.executemany(
            "INSERT INTO trades(run_id, date, symbol, side, price, notional, weight, reason) "
            "VALUES (?,?,?,?,?,?,?,?)", rows)
        conn.commit()

    def get_trades(self, run_id: int | None = None, limit: int = 200) -> pd.DataFrame:
        conn = self._conn_ensure()
        if run_id is None:
            df = pd.read_sql_query(
                "SELECT * FROM trades ORDER BY id DESC LIMIT ?", conn, params=(limit,))
        else:
            df = pd.read_sql_query(
                "SELECT * FROM trades WHERE run_id=? ORDER BY id DESC LIMIT ?",
                conn, params=(run_id, limit))
        return df

    # ---- positions ----
    def record_positions(self, run_id: int, positions: pd.DataFrame) -> None:
        conn = self._conn_ensure()
        sym_group = get_settings().universe_flat
        rows = []
        for date, row in positions.iterrows():
            for sym, w in row.items():
                if abs(w) > 1e-6:
                    rows.append((run_id, str(date.date()), sym, float(w), sym_group.get(sym, "其他")))
        conn.executemany(
            "INSERT INTO positions(run_id, date, symbol, weight, industry) VALUES (?,?,?,?,?)", rows)
        conn.commit()

    # ---- snapshots ----
    def record_snapshot(self, run_id: int, date: str, metrics: dict[str, Any],
                        benchmark_nav: float | None = None) -> None:
        conn = self._conn_ensure()
        conn.execute(
            "INSERT INTO snapshots(run_id, date, nav, total_return, annual_return, sharpe, "
            "max_drawdown, benchmark_nav) VALUES (?,?,?,?,?,?,?,?)",
            (run_id, date,
             metrics.get("final_nav", 0.0),
             metrics.get("total_return", 0.0),
             metrics.get("annual_return", 0.0),
             metrics.get("sharpe", 0.0),
             metrics.get("max_drawdown", 0.0),
             benchmark_nav),
        )
        conn.commit()

    def get_latest_snapshot(self) -> pd.DataFrame:
        conn = self._conn_ensure()
        return pd.read_sql_query(
            "SELECT * FROM snapshots ORDER BY id DESC LIMIT 1", conn)

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
