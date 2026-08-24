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
    p_voice.add_argument("--no-stream", action="store_true", help="关闭流式输出，改为整段打印")
    p_voice.add_argument("--history-file", help="覆盖对话历史文件路径")

    p_camel = sub.add_parser("camel", help="CAMEL × DeepSeek 对话智能体")
    p_camel.add_argument("--user", help="覆盖用户称呼")

    sub.add_parser("agent", help="工具调用 ReAct 智能体（可计算/时钟/骰子）")

    p_web = sub.add_parser("web", help="多模型 Web 界面（FastAPI + 玻璃拟态前端）")
    p_web.add_argument("--host", default="127.0.0.1", help="监听地址")
    p_web.add_argument("--port", type=int, default=8000, help="监听端口")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    settings = Settings.from_env()
    settings.validate()
    setup_logging(build_log_level(settings.log_level))

    if args.command == "voice":
        if args.no_speak:
            settings.speak_enabled = False
        if args.no_stream:
            settings.stream_mode = False
        if args.history_file:
            settings.history_file = args.history_file
        from .assistant import VoiceAssistant

        VoiceAssistant(settings).run()

    elif args.command == "camel":
        if args.user:
            settings.camel_user_name = args.user
        from .camel_agent import CamelChatAgent

        CamelChatAgent(settings).run()

    elif args.command == "agent":
        from .agentic import ToolAgent

        ToolAgent(settings).run()

    elif args.command == "web":
        from .web import run as run_web

        run_web(host=args.host, port=args.port)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
