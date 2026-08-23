# ❓ FAQ

## 配置与密钥

**Q：如何配置 API Key？**
A：复制 `.env.example` 为 `.env`，填入 `DEEPSEEK_API_KEY`；或直接设置环境变量。密钥**只从环境读取**，绝不硬编码/入库。

**Q：忘了配置 Key 会怎样？**
A：启动即抛 `RuntimeError`，提示你设置 `DEEPSEEK_API_KEY`。不会运行到一半才报错。

## 运行

**Q：没有 NVIDIA GPU 能跑吗？**
A：本项目不依赖本地 GPU——它调用 DeepSeek API，只要有网络即可。语音播报需要系统有音频输出设备。

**Q：没有音频环境（如容器/CI）会怎样？**
A：TTS 用 `--no-speak` 关掉，或缺失 `edge-tts` 时自动降级（仅打日志），对话功能不受影响。

**Q：记忆存在哪里？**
A：默认用户级 `~/.dsh_assistant/conversation_history.json`。可用 `DSH_DATA_DIR` 或 `--history-file` 覆盖。

## 依赖

**Q：`camel-ai` 没装，报错怎么办？**
A：`camel` 子命令需要 `camel-ai`，未装会提示 `pip install camel-ai`（或 `pip install -e ".[camel]"`）。`voice` 子命令不受影响。

**Q：`openai` / `edge-tts` 必须装吗？**
A：`openai`（LLM）与 `edge-tts`（语音）是功能依赖；包本身永远可导入。缺 `openai` 时 LLM 调用会提示安装。

## 定制

**Q：怎么换模型/声音/温度？**
A：通过环境变量：`DSH_MODEL`、`DSH_VOICE`、`DSH_TEMPERATURE`（见 `.env.example`）。

**Q：怎么改角色人设？**
A：`Settings.voice_system_prompt` / `camel_system_prompt`（源自 [`prompts.py`](prompts.py)）。

## 质量与贡献

**Q：如何跑测试？**
A：`pip install -e ".[dev]"` 后 `pytest -q`。测试零网络、零三方依赖。

**Q：CI 跑什么？**
A：`.github/workflows/ci.yml` 跑 `pytest` + `py_compile` + `ruff check src tests`。

**Q：想贡献怎么开始？**
A：Fork、开分支、补测试（不依赖 GPU/网络）、过 `ruff` 后提交 PR。
