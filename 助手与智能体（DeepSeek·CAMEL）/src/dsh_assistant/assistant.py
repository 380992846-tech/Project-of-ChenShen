"""语音助手（DeepSeek + Edge TTS），组合 LLM、TTS 与记忆。"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from .config import Settings
from .llm import LLMClient, LLMError
from .memory import MemoryStore
from .prompts import VOICE_HELP
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
        return False

    def _print_history(self, n: int) -> None:
        print(f"--- 最近 {n} 条 ---")
        for msg in self.memory.recent(n):
            content = str(msg.get("content", ""))[:50]
            print(f"{msg.get('role', '?')}: {content}...")

    def run(self) -> None:
        print(f"🎓 小DeepSeek（贵系人）已启动。我的声音是：{self.settings.voice}")
        print(self.greet())
        print("💬 输入 /help 查看命令，输入 /quit 退出。\n")
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
            reply = self.chat(user_input)
            print(f"🤖 小DeepSeek：{reply}")
            self.speak(reply)
