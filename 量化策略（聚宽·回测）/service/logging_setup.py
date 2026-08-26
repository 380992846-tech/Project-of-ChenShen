"""
service/logging_setup.py
========================

日志初始化：优先用 loguru，缺失时回退标准 logging。统一、可读、可分环境。

用法
----
    from 量化系统.service.logging_setup import get_logger
    logger = get_logger(__name__)
    logger.info("hello")
"""

from __future__ import annotations

import logging
import sys

try:  # pragma: no cover - 取决于是否安装 loguru
    from loguru import logger as _loguru_logger

    _HAS_LOGURU = True

    _loguru_logger.remove()
    _loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | <cyan>{name}</cyan> | {message}",
        level="INFO",
    )
except Exception:  # pragma: no cover
    _HAS_LOGURU = False
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )


def get_logger(name: str = "quant_system"):
    """返回日志器。若安装了 loguru 则给一个绑定 name 的代理，否则用标准 logging。"""
    if _HAS_LOGURU:
        return _loguru_logger.bind(name=name)
    return logging.getLogger(name)
