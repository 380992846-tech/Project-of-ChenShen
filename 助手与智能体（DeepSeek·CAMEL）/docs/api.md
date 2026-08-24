# 🔧 API 参考

以下为公开接口。所有示例基于 `import dsh_assistant`。

## 配置

### `config.Settings`
数据类，聚合全部配置。敏感项（`api_key`）只从环境读取。

- `Settings.from_env()` → `Settings`：加载 `.env`（若安装了 `python-dotenv`）再从环境变量构造。
- `settings.validate()`：缺 `DEEPSEEK_API_KEY` 时抛 `RuntimeError`（含修复指引）。
- `settings.history_path` → `Path`：记忆文件路径。
- `settings.model_ids() -> dict[str, str]`：`key → 模型标识`（`pro/flash/vision`），未配置回退 `settings.model`。
- `settings.model_catalog() -> list[dict]`：前端目录（含 `label` 与解析后 `model_id`）。
- `config.MODEL_CATALOG`：`[{key, label}]`，当前为 V4 Pro / V4 Flash / V4 Flash 视觉。
- `config.build_log_level(level: str) -> int`：字符串级别 → `logging` 常量。

```python
from dsh_assistant.config import Settings, build_log_level
s = Settings.from_env()
s.validate()
print(s.model_ids())     # {'pro': ..., 'flash': ..., 'vision': ...}
```

## 记忆

### `memory.MemoryStore(path, system_prompt, max_rounds)`
- `m.add(role, content)`：追加并原子保存 + 裁剪。
- `m.clear()`：清空（保留 1 条 system）。
- `m.snapshot() -> list[dict]`：返回当前消息列表。
- `m.recent(n) -> list[dict]`：返回最近 n 条。
- `m.is_empty() -> bool`：是否仅剩 system。
- `m.last_pair() -> tuple[str, str] | None`：最近一轮 (用户, 助手)。
- `m.replace_last_assistant(content) -> bool`：覆盖最后一条助手回复。

```python
from dsh_assistant.memory import MemoryStore
m = MemoryStore(Path("/tmp/h.json"), "你是助手", max_rounds=20)
m.add("user", "hi")
m.add("assistant", "hello")
m.replace_last_assistant("你好呀")
```

## LLM

### `llm.LLMClient(settings)`
- `client.chat(messages, model=None) -> str`：一次性返回文本；`model` 可覆盖 `settings.model`。
- `client.stream(messages, model=None) -> Iterator[str]`：流式逐段产出文本增量。
- `client.chat_with_tools(messages, tools, model=None) -> (text | None, tool_calls)`：原生 function-calling；`tool_calls` 为 `[{id, name, arguments(dict)}]`。

```python
from dsh_assistant.llm import LLMClient
llm = LLMClient(settings)
print(llm.chat([{"role": "user", "content": "你好"}], model="deepseek-chat"))
for chunk in llm.stream([{"role": "user", "content": "你好"}], model="deepseek-chat"):
    print(chunk, end="", flush=True)
```

## 工具

### `tools`
- `tools.safe_calculate(expr) -> float`：安全求值（`ast` 白名单，绝不 `eval`）。
- `tools.tool_schemas() -> list[dict]`：OpenAI 风格工具定义（current_time / calculate / roll_dice）。
- `tools.run_tool(name, args) -> str`：执行工具，未知工具返回提示。

## 工具智能体

### `agentic.ToolAgent(settings)`
- `agent.chat(text, model=None) -> str`：ReAct 循环，内部调用工具并回传结果。
- `agent.rewrite_last(model=None) -> str | None`：重写并覆盖最后一条助手回复。
- `agent.clear_history()`：清空历史。
- `agent.run()`：交互循环（`/help` `/clear` `/rewrite` `/quit`）。

```python
from dsh_assistant.agentic import ToolAgent
agent = ToolAgent(settings)
print(agent.chat("算一下 (2+3)*5，再掷一个骰子。"))
```

## TTS

### `tts.TTSEngine(settings)`
- `engine.speak(text)`：后台线程异步播报。

## 语音助手

### `assistant.VoiceAssistant(settings)`
- `va.greet() -> str`：按时间问候。
- `va.chat(text) -> str`：LLM 回复（带记忆），失败返回兜底文案。
- `va.chat_stream(text, display=True) -> str`：流式生成并返回完整回复。
- `va.rewrite_last() -> str | None`：重写并覆盖上一条回复。
- `va.speak(text)`：播报。
- `va.run()`：交互循环（`/help` `/clear` `/history` `/rewrite` `/quit`）。

## CAMEL 智能体

### `camel_agent.CamelChatAgent(settings)`
- `agent.chat(text) -> str`：基于 CAMEL 的对话回复（带上下文）。
- `agent.rewrite_last() -> str | None`：重写并覆盖上一条回复。
- `agent.run()`：交互循环（`/help` `/clear` `/rewrite` `/quit`）。
- 未安装 `camel-ai` 时使用会抛 `RuntimeError` 提示安装。

## Web 后端

### `web.app`（FastAPI）
- `GET  /`                 → 玻璃拟态前端页面（`web/index.html`）。
- `GET  /api/meta`         → `{models, modes}`。
- `POST /api/chat`         → `{reply}`（`session/mode/model/message`）。
- `POST /api/chat/stream`  → SSE 流式（`data: {"type":"text"/"done"/"error"}`）。
- `POST /api/rewrite`      → `{reply}`（覆盖上一条回复）。
- `POST /api/clear`        → `{ok}`（清空当前模式上下文）。
- `POST /api/tts`          → `audio/mpeg`（Edge TTS 合成）。

### `web.run(host, port, reload)`
以 `uvicorn` 启动 `web.app`。

## CLI

### `cli.main(argv: list[str] | None = None) -> int`
- `dsh-assistant voice [--no-speak] [--no-stream] [--history-file PATH]`
- `dsh-assistant camel [--user NAME]`
- `dsh-assistant agent`
- `dsh-assistant web [--host HOST] [--port PORT]`
