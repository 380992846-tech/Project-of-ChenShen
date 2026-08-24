"""集中式配置管理与环境变量加载。

为整个包提供统一的 `Settings`，从 `.env` / 环境变量读取并校验敏感项。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .prompts import AGENT_SYSTEM_PROMPT, CAMEL_SYSTEM_PROMPT, CAMEL_USER_NAME, VOICE_SYSTEM_PROMPT

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:  # pragma: no cover
    load_dotenv = None  # type: ignore


# 项目根目录（src/..）
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# 默认数据目录：用户级，不污染仓库
DEFAULT_DATA_DIR = Path.home() / ".dsh_assistant"

# 前端可选的模型目录。label 用于界面展示；key 是稳定标识；
# model_id 为空时回退到 ``settings.model``（DSH_MODEL）。
MODEL_CATALOG: list[dict[str, str]] = [
    {"key": "pro", "label": "V4 Pro"},
    {"key": "flash", "label": "V4 Flash"},
    {"key": "vision", "label": "V4 Flash 视觉"},
]


def _resolve_data_dir(configured: str | None) -> Path:
    """数据目录解析：显式配置 > 环境变量 > 用户级默认值。"""
    if configured:
        return Path(configured).expanduser()
    if os.environ.get("DSH_DATA_DIR"):
        return Path(os.environ["DSH_DATA_DIR"]).expanduser()
    return DEFAULT_DATA_DIR


@dataclass
class Settings:
    """应用配置。

    所有敏感项（API Key）只从环境变量或 `.env` 读取，绝不硬编码。
    """

    # 运行时
    log_level: str = "INFO"

    # LLM（DeepSeek）
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int | None = None
    request_timeout: float = 60.0
    max_retries: int = 3
    retry_backoff: float = 1.0

    # 语音（Edge TTS）
    voice: str = "zh-CN-YunxiNeural"
    speak_enabled: bool = True
    # 输出模式
    stream_mode: bool = True

    # 多模型：各模型的 API model 标识（可留空，回退到 ``model``）
    model_pro: str = ""
    model_flash: str = ""
    model_vision: str = ""

    # 记忆
    max_rounds: int = 20
    history_file: str | None = None
    data_dir: Path = field(default_factory=lambda: DEFAULT_DATA_DIR)

    # CAMEL
    camel_system_prompt: str = CAMEL_SYSTEM_PROMPT
    camel_user_name: str = CAMEL_USER_NAME
    camel_max_history: int = 10

    # 工具智能体（ToolAgent）
    agent_system_prompt: str = AGENT_SYSTEM_PROMPT
    agent_max_history: int = 12

    # 语音助手人设
    voice_system_prompt: str = VOICE_SYSTEM_PROMPT

    @classmethod
    def from_env(cls) -> Settings:
        """从环境变量 / `.env` 构造设置。"""
        if load_dotenv is not None:
            load_dotenv()
        s = cls(
            log_level=os.environ.get("DSH_LOG_LEVEL", "INFO"),
            api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
            base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            model=os.environ.get("DSH_MODEL", "deepseek-chat"),
            temperature=float(os.environ.get("DSH_TEMPERATURE", "0.7")),
            max_tokens=int(os.environ["DSH_MAX_TOKENS"]) if os.environ.get("DSH_MAX_TOKENS") else None,
            voice=os.environ.get("DSH_VOICE", "zh-CN-YunxiNeural"),
            speak_enabled=os.environ.get("DSH_SPEAK", "1") not in ("0", "false", "False", "no"),
            stream_mode=os.environ.get("DSH_STREAM", "1") not in ("0", "false", "False", "no"),
            model_pro=os.environ.get("DSH_MODEL_PRO", ""),
            model_flash=os.environ.get("DSH_MODEL_FLASH", ""),
            model_vision=os.environ.get("DSH_MODEL_VISION", ""),
            max_rounds=int(os.environ.get("DSH_MAX_ROUNDS", "20")),
            data_dir=_resolve_data_dir(os.environ.get("DSH_DATA_DIR")),
        )
        return s

    def validate(self) -> None:
        """校验必填配置；缺失时抛出含修复指引的异常。"""
        if not self.api_key:
            raise RuntimeError(
                "缺少 DEEPSEEK_API_KEY。请设置环境变量，或复制 .env.example 为 .env 并填入你的 Key。"
            )

    @property
    def history_path(self) -> Path:
        """返回对话历史文件路径。"""
        if self.history_file:
            return Path(self.history_file).expanduser()
        return self.data_dir / "conversation_history.json"

    def model_ids(self) -> dict[str, str]:
        """返回 key -> 模型标识；未配置时回退到 ``self.model``。"""
        overrides = {"pro": self.model_pro, "flash": self.model_flash, "vision": self.model_vision}
        return {key: override or self.model for key, override in overrides.items()}

    def model_catalog(self) -> list[dict[str, str]]:
        """返回带解析后模型标识的前端目录。"""
        ids = self.model_ids()
        return [{**entry, "model_id": ids[entry["key"]]} for entry in MODEL_CATALOG]


def build_log_level(level: str) -> int:
    """把字符串日志级别映射为 logging 常量。"""
    import logging

    mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return mapping.get(level.upper(), logging.INFO)
