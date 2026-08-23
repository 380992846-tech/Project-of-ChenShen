"""对话记忆：线程安全 + 原子持久化到 JSON。"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import threading
from pathlib import Path

logger = logging.getLogger(__name__)


class MemoryStore:
    """把 OpenAI 风格的消息列表持久化到 JSON，支持裁剪与清空。

    - 线程安全（所有写操作加锁）；
    - 原子写（临时文件 + os.replace），避免写一半损坏；
    - 自动保留 1 条 system + 最近 ``max_rounds`` 轮。
    """

    def __init__(self, path: Path, system_prompt: str, max_rounds: int):
        self.path = Path(path)
        self.system_prompt = system_prompt
        self.max_rounds = max_rounds
        self._lock = threading.Lock()
        self.messages: list[dict[str, str]] = []
        self._load()
        if not self.messages:
            self.messages.append({"role": "system", "content": system_prompt})

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.messages = [m for m in data if isinstance(m, dict)]
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("加载历史失败，将重新开始: %s", exc)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    def _trim(self) -> None:
        if len(self.messages) > 1 + 2 * self.max_rounds:
            self.messages = [self.messages[0]] + self.messages[-(2 * self.max_rounds):]

    # ---- 公开 API ----
    def add(self, role: str, content: str) -> None:
        with self._lock:
            self.messages.append({"role": role, "content": content})
            self._trim()
            self._save()

    def clear(self) -> None:
        with self._lock:
            self.messages = [self.messages[0]] if self.messages else [
                {"role": "system", "content": self.system_prompt}
            ]
            self._save()

    def snapshot(self) -> list[dict[str, str]]:
        with self._lock:
            return list(self.messages)

    def recent(self, n: int) -> list[dict[str, str]]:
        with self._lock:
            return list(self.messages[-n:])

    def is_empty(self) -> bool:
        with self._lock:
            return len(self.messages) <= 1
