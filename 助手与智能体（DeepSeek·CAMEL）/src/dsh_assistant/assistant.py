"""语音助手（DeepSeek + Edge TTS），组合 LLM、TTS 与记忆。"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from .config import Settings
from .llm import LLMClient, LLMError
from .memory import MemoryStore
from .prompts import REWRITE_INSTRUCTION, VOICE_HELP
from .tts import TTSEngine

logger = logging.getLogger(__name__)


class VoiceAssistant:
    """带命令系统、持久化记忆与可选语音播报的助手。"""

    def __init__(self, settings: Settings):
        settings.validate()
        self.settings = settings
        self.llm = LLMClient(settings)
        self.tts = TTSEngine(settings)
        self.memory = MemoryStore(
            settings.history_path,
            settings.voice_system_prompt,
            settings.max_rounds,
        )

    def greet(self) -> str:
        hour = datetime.now(tz=timezone.utc).astimezone().hour
        if hour < 12:
            return "兄弟，早上好。又是充满希望的一天。"
        if hour < 18:
            return "兄弟，下午好。我在。"
        return "兄弟，晚上好。清华的月亮，今天也很亮。"

    def chat(self, text: str) -> str:
        self.memory.add("user", text)
        try:
            reply = self.llm.chat(self.memory.snapshot())
        except LLMError as exc:
            logger.warning("对话失败: %s", exc)
            reply = f"兄弟，我遇到点问题：{exc}。你先忙，我重启一下就好。"
        self.memory.add("assistant", reply)
        return reply

    def chat_stream(self, text: str, display: bool = True) -> str:
        """流式对话：逐段打印（可选）并返回完整回复，同时写入记忆。"""
        self.memory.add("user", text)
        parts: list[str] = []
        try:
            for chunk in self.llm.stream(self.memory.snapshot()):
                parts.append(chunk)
                if display:
                    print(chunk, end="", flush=True)
            if display:
                print()
        except LLMError as exc:
            logger.warning("流式对话失败: %s", exc)
            reply = f"兄弟，我遇到点问题：{exc}。你先忙，我重启一下就好。"
        else:
            reply = "".join(parts).strip() or "（这次我没说出话来…）"
        self.memory.add("assistant", reply)
        return reply

    def rewrite_last(self) -> str | None:
        """重写并覆盖最后一条助手回复；无足量上下文时返回 None。"""
        pair = self.memory.last_pair()
        if pair is None:
            return None
        question, previous = pair
        messages = [
            {"role": "system", "content": self.settings.voice_system_prompt},
            {
                "role": "user",
                "content": f"上一轮用户问题：\n{question}\n\n上一轮助手回复：\n{previous}\n\n{REWRITE_INSTRUCTION}",
            },
        ]
        try:
            new = self.llm.chat(messages)
        except LLMError as exc:
            logger.warning("重写失败: %s", exc)
            return None
        self.memory.replace_last_assistant(new)
        return new

    def speak(self, text: str) -> None:
        self.tts.speak(text)

    def _handle_command(self, user_input: str) -> bool:
        """处理命令；返回 True 表示已处理（不当作普通消息）。"""
        cmd = user_input.strip().lower()
        if cmd in ("quit", "/quit", "exit"):
            self.speak("兄弟，再见。我在清华等你回来。")
            return True
        if cmd in ("/help", "help"):
            print(VOICE_HELP)
            return True
        if cmd == "/clear":
            self.memory.clear()
            print("已清空对话记忆。")
            return True
        if cmd == "/history":
            self._print_history(5)
            return True
        if cmd == "/rewrite":
            new = self.rewrite_last()
            if new is None:
                print("兄弟，上一轮还没什么可重写的，先说点什么吧。")
            else:
                print(f"🤖 小DeepSeek（已覆盖）：{new}")
            return True
        return False

    def _print_history(self, n: int) -> None:
        print(f"--- 最近 {n} 条 ---")
        for msg in self.memory.recent(n):
            content = str(msg.get("content", ""))[:50]
            print(f"{msg.get('role', '?')}: {content}...")

    def run(self) -> None:
        print(f"🎓 小DeepSeek（贵系人）已启动。我的声音是：{self.settings.voice}")
        print(self.greet())
        stream_note = "流式" if self.settings.stream_mode else "整段"
        print(f"💬 输入 /help 查看命令，输入 /quit 退出。（{stream_note}输出）\n")
        while True:
            try:
                user_input = input("\n🎤 你：").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                continue
            if self._handle_command(user_input):
                if user_input.strip().lower() in ("quit", "/quit", "exit"):
                    break
                continue
            if self.settings.stream_mode:
                print("🤖 小DeepSeek：", end="", flush=True)
                reply = self.chat_stream(user_input)
            else:
                reply = self.chat(user_input)
                print(f"🤖 小DeepSeek：{reply}")
            self.speak(reply)
