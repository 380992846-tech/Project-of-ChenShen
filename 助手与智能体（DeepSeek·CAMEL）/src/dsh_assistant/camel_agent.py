"""CAMEL × DeepSeek 对话智能体（带上下文历史与命令）。

`camel-ai` 为重量依赖，采用懒加载：未安装时模块仍可导入，只在真正使用时给出明确提示。
"""

from __future__ import annotations

import logging
from typing import Any

from .config import Settings
from .prompts import CAMEL_HELP

logger = logging.getLogger(__name__)


class CamelChatAgent:
    """基于 CAMEL ChatAgent 的带记忆对话智能体。"""

    def __init__(self, settings: Settings):
        settings.validate()
        self.settings = settings
        self.history: list[tuple[str, str]] = []
        self._camel: dict[str, Any] | None = None
        self._agent: Any | None = None

    def _ensure_camel(self) -> dict[str, Any]:
        """懒加载 camel-ai 并缓存类对象。"""
        if self._camel is None:
            try:
                from camel.agents import ChatAgent
                from camel.messages import BaseMessage
                from camel.models import ModelFactory
                from camel.types import ModelPlatformType, ModelType
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "未安装 camel-ai。请执行：pip install camel-ai"
                ) from exc
            self._camel = {
                "ChatAgent": ChatAgent,
                "BaseMessage": BaseMessage,
                "ModelFactory": ModelFactory,
                "ModelPlatformType": ModelPlatformType,
                "ModelType": ModelType,
            }
        return self._camel

    def _get_agent(self) -> Any:
        if self._agent is None:
            c = self._ensure_camel()
            model = c["ModelFactory"].create(
                model_platform=c["ModelPlatformType"].DEEPSEEK,
                model_type=c["ModelType"].DEEPSEEK_CHAT,
                model_config_dict={"temperature": self.settings.temperature},
            )
            self._agent = c["ChatAgent"](model=model, system_message=self.settings.camel_system_prompt)
        return self._agent

    def _context(self):
        c = self._ensure_camel()
        user = self.settings.camel_user_name
        msgs = []
        for role, content in self.history[-2 * self.settings.camel_max_history:]:
            if role == user:
                msgs.append(c["BaseMessage"].make_user_message(role_name=user, content=content))
            else:
                msgs.append(c["BaseMessage"].make_assistant_message(role_name=role, content=content))
        return msgs

    def chat(self, text: str) -> str:
        user = self.settings.camel_user_name
        self.history.append((user, text))
        response = self._get_agent().step(self._context())
        reply = str(response.msg.content)
        self.history.append(("陈深", reply))
        return reply

    def run(self) -> None:
        user = self.settings.camel_user_name
        print("陈深: 晓晓，我来了。（眨眨眼）\n")
        print("💬 输入 /help 查看命令，/quit 退出。\n")
        while True:
            try:
                user_input = input(f"{user}: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                print("陈深: 嗯？晓晓想说什么？（歪头看着你）\n")
                continue
            if user_input.lower() in ("exit", "quit", "退出", "bye", "/quit"):
                print("陈深: 嗯，下次见。记得写代码。（挥手）")
                break
            if user_input in ("/help", "help"):
                print(CAMEL_HELP)
                continue
            if user_input == "/clear":
                self.history.clear()
                print("陈深: 记忆清空啦，重新开始。（眨眨眼）")
                continue
            try:
                reply = self.chat(user_input)
            except Exception as exc:  # noqa: BLE001
                reply = f"（智能体出错了：{exc}）"
                logger.warning("CAMEL 调用失败: %s", exc)
            print(f"陈深: {reply}")
