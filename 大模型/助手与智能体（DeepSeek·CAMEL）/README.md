# 助手与智能体（DeepSeek · CAMEL）

> 两个基于大模型 API 的助手/智能体项目，均已**深化**为可复用类 + 命令系统。

## 项目一：语音助手 `voice_assistant.py`

**DeepSeek API + Edge TTS** 的智能语音助手。

- 🎙️ **语音对话**：DeepSeek 生成回复，Edge TTS 播报（中文女声 `zh-CN-YunxiNeural`）；
- 🧠 **持久化记忆**：对话历史自动存到 `data/conversation_history.json`，重启不丢；
- ⌨️ **命令系统**：`/help`、`/clear`、`/history`、`/quit`；
- 🕐 按时间智能问候，可开关语音播报。

```bash
export DEEPSEEK_API_KEY="your-key"
python 大模型/助手与智能体（DeepSeek·CAMEL）/voice_assistant.py
```

## 项目二：CAMEL 智能体 `camel_chat.py`

基于 **CAMEL 框架 + DeepSeek** 的对话智能体。

- 🤖 **CAMEL 多智能体框架**：`ChatAgent` + 角色化人设（"陈深"）；
- 🧵 **显式上下文历史**：多轮对话有记忆（`/clear` 可清空）；
- ⌨️ **命令系统**：`/help`、`/clear`、`/quit`；
- ⚙️ 可配置人设、温度、历史长度。

```bash
export DEEPSEEK_API_KEY="your-key"
python 大模型/助手与智能体（DeepSeek·CAMEL）/camel_chat.py
```

## 依赖

```bash
pip install openai edge-tts camel-ai   # 见仓库 requirements.txt
```

## 安全

两个项目都**从环境变量 `DEEPSEEK_API_KEY` 读取密钥**，绝不硬编码进代码/仓库。
