# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/) 与[语义化版本](https://semver.org/)。
所有重大变更均记录于此。

## [Unreleased]

### 计划
- 端到端集成测试（真实 LLM / TTS）
- 更多 CAMEL 角色模板与场景
- 对话统计 / 遥测导出

## [0.1.0] - 2026-08-23

### Added
- 标准 Python 包（`src` 布局）与统一 CLI：`dsh-assistant voice|camel`
- 集中配置：`.env` + `Settings` + `validate()`（密钥仅从环境读取）
- 结构化日志（`logging_setup`）
- LLM 客户端：超时 + 指数退避重试（`llm.py`）
- Edge TTS 引擎：懒加载、后台线程、跨平台播放（`tts.py`）
- 线程安全 + 原子写的对话记忆（`memory.py`）
- CAMEL 对话智能体（`camel_agent.py`，懒加载 `camel-ai`）
- 语音助手编排（`assistant.py`）
- 单元测试（12 个，零网络 / 零三方依赖）
- CI（ruff + pytest + compile，`.github/workflows/ci.yml`）
- 工程配置：`pyproject.toml`、`requirements.txt`、`.env.example`、`.gitignore`、`.editorconfig`、`LICENSE`
- 文档：[`docs/architecture.md`](docs/architecture.md)、[`docs/api.md`](docs/api.md)、[`docs/design.md`](docs/design.md)、[`docs/faq.md`](docs/faq.md)

### Changed
- 由两个独立脚本重构为可复用包，原脚本移入 `examples/`
- 对话记忆默认改为用户级目录 `~/.dsh_assistant`（不污染仓库）
- 密钥改为仅在环境变量 / `.env` 中提供，杜绝硬编码

---

参考：[项目目录](https://github.com/380992846-tech/Project-of-ChenShen/tree/main/%E5%8A%A9%E6%89%8B%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%EF%BC%88DeepSeek%C2%B7CAMEL%EF%BC%89) · [Keep a Changelog](https://keepachangelog.com/)
