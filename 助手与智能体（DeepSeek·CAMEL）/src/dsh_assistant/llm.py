"""LLM 客户端：封装 DeepSeek (OpenAI 兼容) API，内置超时与指数退避重试。"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class LLMError(RuntimeError):
    """LLM 调用最终失败。"""


class LLMClient:
    """对 DeepSeek chat completions 的薄封装。

    - 懒加载 `openai`，未安装时给出清晰提示；
    - 内置超时与指数退避重试；
    - 出错时记录上下文，避免静默吞掉。
    """

    def __init__(self, settings: Any):
        self.settings = settings
        self._client: Any | None = None

    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:  # pragma: no cover
                raise LLMError("未安装 openai。请执行：pip install openai") from exc
            self._client = OpenAI(
                api_key=self.settings.api_key,
                base_url=self.settings.base_url,
                timeout=self.settings.request_timeout,
            )
        return self._client

    def chat(self, messages: list[dict[str, str]]) -> str:
        """调用对话补全，返回助手文本。"""
        client = self._get_client()
        kwargs: dict[str, Any] = {
            "model": self.settings.model,
            "messages": messages,
        }
        if self.settings.max_tokens:
            kwargs["max_tokens"] = self.settings.max_tokens

        last_error: Exception | None = None
        for attempt in range(1, self.settings.max_retries + 1):
            try:
                resp = client.chat.completions.create(**kwargs)
                reply = resp.choices[0].message.content
                if reply is None:
                    raise LLMError("模型返回空内容")
                return str(reply)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("LLM 调用失败 (第 %s/%s 次): %s", attempt, self.settings.max_retries, exc)
                if attempt == self.settings.max_retries:
                    break
                time.sleep(self.settings.retry_backoff * (2 ** (attempt - 1)))

        raise LLMError(f"LLM 调用在 {self.settings.max_retries} 次尝试后仍然失败") from last_error
