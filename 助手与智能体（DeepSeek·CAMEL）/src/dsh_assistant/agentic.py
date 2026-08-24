"""工具调用智能体：用 DeepSeek 原生 function-calling 实现 ReAct 循环。

流程：
1. 发送上下文 + 工具定义；
2. 若模型返回工具调用，则执行 ``tools.run_tool`` 并把结果回传（``role=tool``）；
3. 循环直到模型给出最终回答，或超过最大轮数。
"""

from __future__ import annotations

import logging
from typing import Any

from .config import Settings
from .llm import LLMClient, LLMError
from .prompts import REWRITE_INSTRUCTION
from .tools import run_tool, tool_schemas

logger = logging.getLogger(__name__)

# OpenAI 兼容的 tool 消息：``role=tool`` 必须带 ``tool_call_id``。
_TOOL_ROLE = "tool"
_ASSISTANT_ROLE = "assistant"


class ToolAgent:
    """带工具调用能力的 ReAct 智能体，可独立持久化（JSON）。"""

    def __init__(self, settings: Settings):
        settings.validate()
        self.settings = settings
        self.llm = LLMClient(settings)
        self.system_prompt = settings.agent_system_prompt
        self.max_tool_rounds = 8
        self.max_history = settings.agent_max_history
        self.history: list[dict[str, str]] = []

    # ---- 历史管理 ----
    def _append(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-2 * self.max_history:]

    def clear_history(self) -> None:
        self.history.clear()

    def _seed_messages(self, text: str) -> list[dict[str, Any]]:
        """构造本轮消息：system + 历史 + 当前用户输入。"""
        messages: list[dict[str, Any]] = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": text})
        return messages

    def chat(self, text: str, model: str | None = None) -> str:
        """处理一条用户输入，返回最终助手回答。"""
        self._append("user", text)
        messages = self._seed_messages(text)
        tools = tool_schemas()
        round_no = 0

        while round_no < self.max_tool_rounds:
            round_no += 1
            try:
                text_out, calls = self.llm.chat_with_tools(messages, tools, model=model)
            except LLMError as exc:
                logger.warning("工具智能体调用失败: %s", exc)
                return f"（智能体出错了：{exc}）"

            if not calls:
                # 模型给出最终回答
                if text_out:
                    self._append(_ASSISTANT_ROLE, text_out)
                    return text_out
                # 无文本也无工具调用：视作空回复
                return "（模型返回了空回复）"

            # 执行工具调用
            # 记录 assistant 的 tool_calls，并逐个执行、回传结果
            messages.append({
                "role": _ASSISTANT_ROLE,
                "content": text_out or "",
                "tool_calls": [
                    {"id": c["id"], "type": "function",
                     "function": {"name": c["name"], "arguments": self._dumps(c["arguments"])}}
                    for c in calls
                ],
            })
            for c in calls:
                result = run_tool(c["name"], c["arguments"])
                messages.append({
                    "role": _TOOL_ROLE,
                    "tool_call_id": c["id"],
                    "content": result,
                })
                logger.debug("工具 %s 调用 ok", c["name"])

        # 超过最大轮数仍未落定：回到模型要一个基于工具结果的总结
        messages.append({"role": "user", "content": "请基于已完成的工具调用结果，直接给出最终回答。"})
        try:
            final_text, _ = self.llm.chat_with_tools(messages, tools, model=model)
            final = final_text or "（超过最大工具轮数，已停止。）"
        except LLMError as exc:  # pragma: no cover
            final = f"（智能体出错了：{exc}）"
        self._append(_ASSISTANT_ROLE, final)
        return final

    @staticmethod
    def _dumps(args: dict[str, Any]) -> str:
        import json

        return json.dumps(args, ensure_ascii=False)

    # ---- 覆盖上一条回复 ----
    def rewrite_last(self, model: str | None = None) -> str | None:
        """重写并覆盖最后一条助手回答；无足量历史时返回 None。"""
        if len(self.history) < 2:
            return None
        prev = self.history[-2]["content"]
        last = self.history[-1]["content"]
        if self.history[-1]["role"] != _ASSISTANT_ROLE:
            return None
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": (
                    f"上一轮用户问题：\n{prev}\n\n"
                    f"上一轮助手回复：\n{last}\n\n"
                    f"{REWRITE_INSTRUCTION}"
                ),
            },
        ]
        try:
            new = self.llm.chat(messages, model=model)
        except LLMError as exc:
            logger.warning("重写失败: %s", exc)
            return None
        self.history[-1]["content"] = new
        return new

    def run(self) -> None:
        from .prompts import AGENT_HELP

        print("🔧 小深（工具智能体）已启动：我能调用计算器、时钟、骰子等工具。")
        print("💬 输入 /help 查看命令，/quit 退出。\n")
        while True:
            try:
                user_input = input("\n宿主：").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                continue
            cmd = user_input.strip().lower()
            if cmd in ("quit", "/quit", "exit", "退出"):
                print("小深：下次见，宿主。")
                break
            if cmd in ("/help", "help"):
                print(AGENT_HELP)
                continue
            if cmd == "/clear":
                self.clear_history()
                print("小深：历史清空啦。")
                continue
            if cmd == "/rewrite":
                new = self.rewrite_last()
                if new is None:
                    print("小深：还没什么可重写的，先说点什么吧。")
                else:
                    print(f"小深·改写：{new}")
                continue
            reply = self.chat(user_input)
            print(f"小深：{reply}")
