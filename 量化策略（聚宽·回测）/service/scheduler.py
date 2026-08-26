"""
service/scheduler.py
====================

任务调度：用 APScheduler 定时执行数据更新、信号生成、交易指令、日终快照。

- 若安装了 APScheduler 则真正起调度；否则提供占位（说明依赖），不影响其余模块。
- 回调统一委托给 :class:`量化系统.service.orchestrator.QuantService` 的对应方法。
"""

from __future__ import annotations

from typing import Callable

from 量化系统.config import get_settings
from 量化系统.service.logging_setup import get_logger

logger = get_logger(__name__)


class SchedulerService:
    def __init__(self, callbacks: dict[str, Callable[[], None]] | None = None):
        self.settings = get_settings()
        self.callbacks = callbacks or {}
        self._scheduler = None
        self._started = False

    def _init_apscheduler(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        sched = BackgroundScheduler(timezone="Asia/Shanghai")
        s = self.settings.scheduler
        for name, cb in self.callbacks.items():
            cron = getattr(s, name, None)
            if cron:
                sched.add_job(cb, "cron", id=name, replace_existing=True,
                              hour=int(cron.split()[0]), minute=int(cron.split()[1]),
                              day_of_week=cron.split()[2] if len(cron.split()) > 2 else "*")
        self._scheduler = sched

    def start(self) -> None:
        if not self.settings.scheduler.enabled:
            logger.info("调度未启用（scheduler.enabled=false），跳过。")
            return
        if self._started:
            return
        try:
            self._init_apscheduler()
        except Exception as exc:
            logger.warning("未安装或初始化 APScheduler（%s），调度功能暂缺。", exc)
            return
        self._scheduler.start()
        self._started = True
        logger.info("调度已启动：%s", list(self.callbacks.keys()))

    def shutdown(self) -> None:
        if self._scheduler is not None:
            self._scheduler.shutdown(wait=False)
