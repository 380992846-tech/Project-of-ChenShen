"""
voice_assistant.py — DeepSeek + Edge TTS 智能语音助手（带记忆与命令）
=====================================================================

深化版：把原脚本改造成可复用类 + 命令系统 + 自动持久化记忆。

功能
----
- 基于 **DeepSeek API + Edge TTS** 的语音对话助手；
- **对话记忆持久化**到 `data/conversation_history.json`，重启不丢；
- **命令系统**：`/help`、`/clear`、`/history`、`/quit`；
- 按时间智能问候，可开关语音播报。

运行
----
```bash
export DEEPSEEK_API_KEY="your-key"
python 大模型/助手与智能体（DeepSeek·CAMEL）/voice_assistant.py
```
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import edge_tts
from openai import OpenAI


@dataclass
class AssistantConfig:
    voice: str = "zh-CN-YunxiNeural"
    model: str = "deepseek-chat"
    max_rounds: int = 20
    speak_enabled: bool = True
    history_file: str | None = None  # None → 默认写到 data/
    system_prompt: str = (
        "你是一个住在清华二校门模型里的智能语音助手。你的名字叫'小DeepSeek'，"
        "是用户（兄弟）的同伴。你说话温和、简洁、带一点书卷气。你称呼用户为'兄弟'。"
        "你的使命是陪他聊天、帮他整理思路、给他鼓励。"
    )


class VoiceAssistant:
    def __init__(self, cfg: AssistantConfig | None = None):
        self.cfg = cfg or AssistantConfig()

        self.api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("请在环境变量 DEEPSEEK_API_KEY 中配置你的 DeepSeek API Key")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

        # 记忆文件默认放到仓库 data/ 目录
        if not self.cfg.history_file:
            self.cfg.history_file = str(
                Path(__file__).resolve().parent.parent.parent / "data" / "conversation_history.json"
            )
        Path(self.cfg.history_file).parent.mkdir(parents=True, exist_ok=True)

        self.history = self._load_history()
        if not self.history:
            self.history.append({"role": "system", "content": self.cfg.system_prompt})

    # ---------------- 记忆 ----------------
    def _load_history(self) -> list[dict]:
        if os.path.exists(self.cfg.history_file):
            try:
                with open(self.cfg.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save_history(self) -> None:
        with open(self.cfg.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def _trim_history(self) -> None:
        # 保留 1 条 system + 最近 max_rounds 轮
        if len(self.history) > 1 + 2 * self.cfg.max_rounds:
            self.history = [self.history[0]] + self.history[-(2 * self.cfg.max_rounds):]

    # ---------------- 语音 ----------------
    def greet(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            return "兄弟，早上好。又是充满希望的一天。"
        if hour < 18:
            return "兄弟，下午好。我在。"
        return "兄弟，晚上好。清华的月亮，今天也很亮。"

    async def _speak_async(self, text: str) -> None:
        communicate = edge_tts.Communicate(text, self.cfg.voice)
        await communicate.save("temp_speech.mp3")
        os.startfile("temp_speech.mp3")  # Windows 播放

    def speak(self, text: str) -> None:
        if not self.cfg.speak_enabled:
            return
        try:
            asyncio.run(self._speak_async(text))
        except Exception as e:  # 无音频环境也能继续
            print(f"（语音播报失败：{e}）")

    # ---------------- 对话 ----------------
    def chat(self, text: str) -> str:
        self.history.append({"role": "user", "content": text})
        try:
            resp = self.client.chat.completions.create(
                model=self.cfg.model, messages=self.history
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            reply = f"兄弟，我遇到点问题：{e}。你先忙，我重启一下就好。"
        self.history.append({"role": "assistant", "content": reply})
        self._trim_history()
        self._save_history()
        return reply

    # ---------------- 交互循环 ----------------
    def run(self) -> None:
        print(f"🎓 小DeepSeek（贵系人）已启动。我的声音是：{self.cfg.voice}")
        print(self.greet())
        print("💬 输入 /help 查看命令，输入 /quit 退出。\n")
        while True:
            try:
                user_input = input("\n🎤 你：").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                continue

            if user_input.lower() in ("quit", "/quit", "exit"):
                self._save_history()
                self.speak("兄弟，再见。我在清华等你回来。")
                break
            if user_input in ("/help", "help"):
                print("命令：/help 帮助 · /clear 清空记忆 · /history 最近5条 · /quit 退出")
                continue
            if user_input == "/clear":
                self.history = [self.history[0]]
                self._save_history()
                print("已清空对话记忆。")
                continue
            if user_input == "/history":
                print("--- 最近 5 条 ---")
                for msg in self.history[-5:]:
                    print(f"{msg['role']}: {msg['content'][:50]}...")
                continue

            reply = self.chat(user_input)
            print(f"🤖 小DeepSeek：{reply}")
            self.speak(reply)


if __name__ == "__main__":
    VoiceAssistant().run()
