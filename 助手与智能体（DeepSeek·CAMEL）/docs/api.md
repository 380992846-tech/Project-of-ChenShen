# 🔧 API 参考

以下为公开接口。所有示例基于 `import dsh_assistant`。

## 配置

### `config.Settings`
数据类，聚合全部配置。敏感项（`api_key`）只从环境读取。

- `Settings.from_env()` → `Settings`：加载 `.env`（若安装了 `python-dotenv`）再从环境变量构造。
- `settings.validate()`：缺 `DEEPSEEK_API_KEY` 时抛 `RuntimeError`（含修复指引）。
- `settings.history_path` → `Path`：记忆文件路径（`history_file` 或 `<data_dir>/conversation_history.json`）。
- `config.build_log_level(level: str) -> int`：字符串级别 → `logging` 常量。

```python
from dsh_assistant.config import Settings, build_log_level
s = Settings.from_env()
s.validate()
print(s.history_path)
```

## 记忆

### `memory.MemoryStore(path, system_prompt, max_rounds)`
- `m.add(role, content)`：追加并原子保存 + 裁剪。
- `m.clear()`：清空（保留 1 条 system）。
- `m.snapshot() -> list[dict]`：返回当前消息列表。
- `m.recent(n) -> list[dict]`：返回最近 n 条。
- `m.is_empty() -> bool`：是否仅剩 system。

```python
from dsh_assistant.memory import MemoryStore
m = MemoryStore(Path("/tmp/h.json"), "你是助手", max_rounds=20)
m.add("user", "hi")
print(m.snapshot())
```

## LLM

### `llm.LLMClient(settings)`
- `client.chat(messages: list[dict[str,str]]) -> str`：调用 chat completions，内置超时与指数退避重试；最终失败抛 `LLMError`。

```python
from dsh_assistant.llm import LLMClient
reply = LLMClient(settings).chat([
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"},
])
```

## TTS

### `tts.TTSEngine(settings)`
- `engine.speak(text)`：后台线程异步播报（未装 edge-tts 或 `speak_enabled=False` 则静默跳过）。

## 语音助手

### `assistant.VoiceAssistant(settings)`
- `va.greet() -> str`：按时间问候。
- `va.chat(text) -> str`：LLM 回复（带记忆），失败返回兜底文案。
- `va.speak(text)`：播报。
- `va.run()`：启动交互循环（`/help` `/clear` `/history` `/quit`）。

## CAMEL 智能体

### `camel_agent.CamelChatAgent(settings)`
- `agent.chat(text) -> str`：基于 CAMEL 的对话回复（带上下文）。
- `agent.run()`：交互循环（`/help` `/clear` `/quit`）。
- 未安装 `camel-ai` 时使用会抛 `RuntimeError` 提示安装。

## CLI

### `cli.main(argv: list[str] | None = None) -> int`
- `dsh-assistant voice [--no-speak] [--history-file PATH]`
- `dsh-assistant camel [--user NAME]`
