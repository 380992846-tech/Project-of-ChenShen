"""确定性工具注册表：供 ``agentic.ToolAgent`` 调用的工具集。

设计原则：
- 全部无副作用、确定性输出，便于测试断言；
- 计算器用 ``ast`` 白名单解析，绝不 ``eval`` 任意表达式；
- 每个工具提供 OpenAI 风格 ``parameters``（JSON Schema），由 LLM 直接消费。
"""

from __future__ import annotations

import ast
import datetime as _dt
import operator
import random
from typing import Any, Callable

# ---- 安全计算器（AST 白名单）----

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_calculate(expr: str) -> str:
    """安全求值一个仅含数字与 ``+ - * / // % ** ( )`` 的表达式。"""
    tree = ast.parse(expr, mode="eval")
    return _calc_node(tree.body)


def _calc_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _calc_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _calc_node(node.left)
        right = _calc_node(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_calc_node(node.operand))
    raise ValueError("表达式包含不被允许的语法")


def current_time(_: dict[str, Any] | None = None) -> str:
    """返回当前本地时间。"""
    now = _dt.datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def calculate(args: dict[str, Any]) -> str:
    """计算一个算术表达式。"""
    expr = args.get("expression", "")
    try:
        result = safe_calculate(expr)
    except (ValueError, SyntaxError, ZeroDivisionError) as exc:
        return f"计算失败：{exc}"
    # 整数化显示更友好
    if float(result).is_integer():
        return f"{expr} = {int(result)}"
    return f"{expr} = {result:.6f}"


def roll_dice(args: dict[str, Any]) -> str:
    """掷骰子：``number`` 个 ``sides`` 面骰。"""
    number = int(args.get("number", 1))
    sides = int(args.get("sides", 6))
    if not (1 <= number <= 20 and 2 <= sides <= 1000):
        return "参数越界：number∈[1,20]，sides∈[2,1000]。"
    rolls = [random.randint(1, sides) for _ in range(number)]
    return f"{number}d{sides} = {rolls}，总和 = {sum(rolls)}"


# ---- 目录 ----

_TOOL_DEFS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "current_time",
            "description": "获取当前本地时间（含时区）。用于问候、定时等需要时间的场景。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算一个算术表达式，仅支持数字与 + - * / // % ** ( )。用于精确计算。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的算术表达式，如 (2+3)*5。",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "roll_dice",
            "description": "掷骰子，返回每个骰子的点数与总和。",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "description": "骰子数量（1-20），默认 1。"},
                    "sides": {"type": "integer", "description": "每个骰子面数（2-1000），默认 6。"},
                },
                "required": [],
            },
        },
    },
]

_HANDLERS: dict[str, Callable[[dict[str, Any]], str]] = {
    "current_time": current_time,
    "calculate": calculate,
    "roll_dice": roll_dice,
}


def tool_schemas() -> list[dict[str, Any]]:
    """返回 OpenAI 风格的工具定义列表，供 ``tools`` 请求参数使用。"""
    return _TOOL_DEFS


def available_names() -> list[str]:
    return sorted(_HANDLERS)


def run_tool(name: str, args: dict[str, Any]) -> str:
    """执行工具并返回字符串结果；未知工具返回明确提示。"""
    handler = _HANDLERS.get(name)
    if handler is None:
        return f"未知工具：{name}（可用：{', '.join(available_names())}）"
    try:
        result = handler(args)
    except Exception as exc:  # noqa: BLE001 —— 工具内部错误回传给模型，而非崩溃
        return f"工具 {name} 执行出错：{exc}"
    return str(result)
