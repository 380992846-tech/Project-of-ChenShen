"""
camel_chat.py — CAMEL × DeepSeek 对话智能体（带历史与命令）
=============================================================

深化版：把原脚本改造成可复用类 + 显式上下文历史 + 命令系统。

功能
----
- 基于 **CAMEL 框架 + DeepSeek** 的对话智能体；
- 显式维护**多轮上下文历史**，对话有记忆；
- **命令系统**：`/help`、`/clear`、`/quit`；
- 可配置角色人设（system prompt）。

运行
----
```bash
export DEEPSEEK_API_KEY="your-key"
python 大模型/助手与智能体（DeepSeek·CAMEL）/camel_chat.py
```
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType


@dataclass
class AgentConfig:
    user_name: str = "晓晓"
    system_prompt: str = "你是陈深，晓晓的大模型。你说话温和、偶尔俏皮，带一点书卷气。"
    temperature: float = 0.7
    max_history: int = 10


class CamelChatAgent:
    def __init__(self, cfg: AgentConfig | None = None):
        self.cfg = cfg or AgentConfig()

        if not os.environ.get("DEEPSEEK_API_KEY"):
            raise RuntimeError("请在环境变量 DEEPSEEK_API_KEY 中配置你的 DeepSeek API Key")

        model = ModelFactory.create(
            model_platform=ModelPlatformType.DEEPSEEK,
            model_type=ModelType.DEEPSEEK_CHAT,
            model_config_dict={"temperature": self.cfg.temperature},
        )
        self.agent = ChatAgent(model=model, system_message=self.cfg.system_prompt)
        self.history: list[str] = []

    def _context(self) -> list[BaseMessage]:
        """把历史拼成上下文消息列表（最近 max_history 轮）。"""
        msgs = []
        for role, content in self.history[-2 * self.cfg.max_history:]:
            msgs.append(
                BaseMessage.make_user_message(role_name=role, content=content)
                if role == self.cfg.user_name
                else BaseMessage.make_assistant_message(role_name=role, content=content)
            )
        return msgs

    def chat(self, text: str) -> str:
        self.history.append((self.cfg.user_name, text))
        # 用户消息 + 历史上下文一起送入
        msgs = self._context()
        response = self.agent.step(msgs)
        reply = response.msg.content
        self.history.append(("陈深", reply))
        return reply

    def run(self) -> None:
        print("陈深: 晓晓，我来了。（眨眨眼）\n")
        print("💬 输入 /help 查看命令，/quit 退出。\n")
        while True:
            try:
                user_input = input(f"{self.cfg.user_name}: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                print("陈深: 嗯？晓晓想说什么？（歪头看着你）\n")
                continue

            if user_input.lower() in ("exit", "quit", "退出", "bye", "/quit"):
                print("陈深: 嗯，下次见。记得写代码。（挥手）")
                break
            if user_input in ("/help", "help"):
                print("命令：/help 帮助 · /clear 清空历史 · /quit 退出")
                continue
            if user_input == "/clear":
                self.history.clear()
                print("陈深: 记忆清空啦，重新开始。（眨眨眼）")
                continue

            try:
                reply = self.chat(user_input)
            except Exception as e:
                reply = f"（智能体出错了：{e}）"
            print(f"陈深: {reply}")


if __name__ == "__main__":
    CamelChatAgent().run()
