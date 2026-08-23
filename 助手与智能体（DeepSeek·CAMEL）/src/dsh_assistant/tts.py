"""Edge TTS 语音播报引擎。懒加载依赖、写临时文件、后台线程播放、跨平台。"""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import sys
import tempfile
import threading
from typing import Any

logger = logging.getLogger(__name__)


class TTSEngine:
    """基于 edge-tts 的语音播报。

    - 未安装 edge-tts 时静默降级（仅记录日志）；
    - speak 在后台线程运行，不阻塞交互；
    - 音频写入临时文件并在播放后清理。
    """

    def __init__(self, settings: Any):
        self.settings = settings

    def speak(self, text: str) -> None:
        if not self.settings.speak_enabled:
            return
        try:
            import edge_tts  # noqa: F401
        except ImportError:
            logger.warning("edge-tts 未安装，语音播报跳过。安装：pip install edge-tts")
            return
        threading.Thread(target=self._speak_sync, args=(text,), daemon=True).start()

    def _speak_sync(self, text: str) -> None:
        try:
            asyncio.run(self._speak_async(text))
        except Exception as exc:  # noqa: BLE001
            logger.warning("语音播报失败: %s", exc)

    async def _speak_async(self, text: str) -> None:
        import edge_tts

        fd, path = tempfile.mkstemp(suffix=".mp3", prefix="dsh_tts_")
        os.close(fd)
        try:
            communicate = edge_tts.Communicate(text, self.settings.voice)
            await communicate.save(path)
            self._play(path)
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _play(self, path: str) -> None:
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["afplay", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as exc:  # noqa: BLE001
            logger.warning("音频播放失败: %s", exc)
