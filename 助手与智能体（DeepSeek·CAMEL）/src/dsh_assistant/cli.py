"""命令行入口：`dsh-assistant voice` 与 `dsh-assistant camel`。"""

from __future__ import annotations

import argparse

from .config import Settings, build_log_level
from .logging_setup import setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dsh-assistant",
        description="DeepSeek · CAMEL 助手与智能体 CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_voice = sub.add_parser("voice", help="DeepSeek + Edge TTS 语音助手")
    p_voice.add_argument("--no-speak", action="store_true", help="关闭语音播报")
    p_voice.add_argument("--history-file", help="覆盖对话历史文件路径")

    p_camel = sub.add_parser("camel", help="CAMEL × DeepSeek 对话智能体")
    p_camel.add_argument("--user", help="覆盖用户称呼")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    settings = Settings.from_env()
    settings.validate()
    setup_logging(build_log_level(settings.log_level))

    if args.command == "voice":
        if args.no_speak:
            settings.speak_enabled = False
        if args.history_file:
            settings.history_file = args.history_file
        from .assistant import VoiceAssistant

        VoiceAssistant(settings).run()

    elif args.command == "camel":
        if args.user:
            settings.camel_user_name = args.user
        from .camel_agent import CamelChatAgent

        CamelChatAgent(settings).run()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
