"""
api/server.py
==============

量化中台 / FastAPI 后端。

暴露接口
--------
- ``GET /api/dashboard`` —— 中台总览（KPI、净值曲线、资产配置、交易流水、信号）。
- ``GET /api/portfolio`` —— 当前持仓与行业配置。
- ``GET /api/signals``   —— 最新交易信号与流水。
- ``GET /api/backtest``  —— 回测绩效摘要。
- ``GET /``              —— 前端页面（数据驱动的 TMT 量化中台）。
- ``POST /api/run``      —— 手动触发一次完整流水。

服务复用 :class:`量化系统.service.orchestrator.QuantService`，运行结果会被缓存。
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, APIRouter, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from 量化系统.config import get_settings, PKG_ROOT
from 量化系统.service.orchestrator import QuantService
from 量化系统.service.logging_setup import get_logger

logger = get_logger(__name__)


class RunRequest(BaseModel):
    strategy: str | None = None


def create_app(service: QuantService | None = None) -> FastAPI:
    settings = get_settings()
    service = service or QuantService(settings)
    app = FastAPI(title="TMT 量化中台", version="0.1.0")
    router = APIRouter(prefix="/api")

    @router.get("/dashboard")
    def dashboard() -> dict[str, Any]:
        return service.dashboard()

    @router.get("/portfolio")
    def portfolio() -> dict[str, Any]:
        return service.portfolio()

    @router.get("/signals")
    def signals() -> dict[str, Any]:
        return service.signals()

    @router.get("/signals/explain")
    def explain_signal(symbol: str = Query(..., description="标的代码，如 512480"),
                       action: str | None = Query(None, description="买入/卖出方向")) -> dict[str, Any]:
        return service.explain_symbol(symbol, action)

    @router.get("/backtest")
    def backtest() -> dict[str, Any]:
        return service.backtest()

    @router.get("/status")
    def status() -> dict[str, Any]:
        d = service.dashboard()
        return {
            "strategy": d.get("strategy"),
            "environment": d.get("environment"),
            "updated_at": d.get("updated_at"),
            "kpis": d.get("kpis"),
        }

    @router.post("/run")
    def run(payload: RunRequest | None = None) -> dict[str, Any]:
        name = payload.strategy if payload else None
        state = service.run(strategy_name=name)
        return state.to_dict()

    app.include_router(router)

    # 静态前端
    web_dir = PKG_ROOT / "web"
    if web_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(web_dir)), name="assets")
        index = web_dir / "index.html"

        @app.get("/", response_class=HTMLResponse)
        def index_html():
            return FileResponse(str(index))
    else:
        @app.get("/", response_class=HTMLResponse)
        def index_html():
            return HTMLResponse("<h1>TMT 量化中台 (未找到 web/index.html)</h1>")

    return app


app = create_app()
