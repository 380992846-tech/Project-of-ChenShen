"""LLM 客户端：封装 DeepSeek (OpenAI 兼容) API，内置超时与指数退避重试。

提供三种调用方式：
- ``chat``          —— 一次性返回完整文本；
- ``stream``        —— 流式逐段返回文本（生成器）；
- ``chat_with_tools`` —— 原生 function-calling，返回 (文本, 工具调用列表)。
"""

from __future__ import annotations

import logging
import time
from collections.abc import Iterator
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

    def _baseline_kwargs(self, messages: list[dict[str, str]], model: str | None = None) -> dict[str, Any]:
        """构造基础请求参数。``model`` 可为空，回退到 ``settings.model``。"""
        kwargs: dict[str, Any] = {
            "model": model or self.settings.model,
            "messages": messages,
        }
        if self.settings.max_tokens:
            kwargs["max_tokens"] = self.settings.max_tokens
        if self.settings.temperature is not None:
            kwargs["temperature"] = self.settings.temperature
        return kwargs

    def chat(self, messages: list[dict[str, str]], model: str | None = None) -> str:
        """调用对话补全，返回助手文本。"""
        kwargs = self._baseline_kwargs(messages, model)

        last_error: Exception | None = None
        for attempt in range(1, self.settings.max_retries + 1):
            try:
                resp = self._get_client().chat.completions.create(**kwargs)
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

    def stream(self, messages: list[dict[str, str]], model: str | None = None) -> Iterator[str]:
        """流式对话补全，逐段产出文本增量。

        注意：流式过程中若出错不会重试（已开始输出），只会抛出 ``LLMError``。
        """
        kwargs = self._baseline_kwargs(messages, model)
        kwargs["stream"] = True
        try:
            stream = self._get_client().chat.completions.create(**kwargs)
        except Exception as exc:
            raise LLMError(f"流式请求失败: {exc}") from exc

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta is None:
                continue
            content = getattr(delta, "content", None)
            if content:
                yield str(content)

    def chat_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        model: str | None = None,
    ) -> tuple[str | None, list[dict[str, Any]]]:
        """原生 function-calling：模型可返回文本，或一系列待执行的工具调用。

        返回 ``(text, tool_calls)``：二者必有其一非空。``text`` 为最终回答，
        ``tool_calls`` 为 ``[{name, arguments(dict)}, ...]`` 解析后的调用列表。
        循环次数由调用方（``agentic.ToolAgent``）控制。
        """
        kwargs = self._baseline_kwargs(messages, model)
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

        last_error: Exception | None = None
        for attempt in range(1, self.settings.max_retries + 1):
            try:
                resp = self._get_client().chat.completions.create(**kwargs)
                message = resp.choices[0].message
                text = str(message.content) if message.content else None
                if not message.tool_calls:
                    return text, []
                calls: list[dict[str, Any]] = []
                for tc in message.tool_calls:
                    calls.append({
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": self._safe_json(tc.function.arguments),
                    })
                return text, calls
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("工具调用失败 (第 %s/%s 次): %s", attempt, self.settings.max_retries, exc)
                if attempt == self.settings.max_retries:
                    break
                time.sleep(self.settings.retry_backoff * (2 ** (attempt - 1)))

        raise LLMError(f"LLM 调用在 {self.settings.max_retries} 次尝试后仍然失败") from last_error

    @staticmethod
    def _safe_json(raw: str | None) -> dict[str, Any]:
        """安全解析工具参数；失败时回退为空 dict，避免整轮报废。"""
        if not raw:
            return {}
        try:
            import json

            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, ValueError):
            return {}
