# 🌌 **从零实现的大模型推理优化 · 分布式系统 · GPU 能效 · 量化交易 · 创意工坊**

—— 清华大学计算机科学与技术系

---

## 📖 关于这个仓库

这不是一个项目，这是一个世界。

这里有**从零手搓的 decoder-only GPT**，有 KV Cache、INT8/INT4/FP8 量化、投机解码、Continuous Batching——每一行代码都有可复现的 benchmark 和单元测试。

这里有**GPU 能效运行时 GEAR**——能耗感知 DVFS、功耗/频率封顶、温度保护与可回收废热度量，把"省电·跑满"做成可度量的工程。

这里有**量化交易策略**，用随机森林、XGBoost+SHAP 在聚宽平台回测，另有**可本地运行**的多资产风险平价策略，含完整特征工程与诊断。

这里有**《陈深的故事》**——用 HTML/CSS/JavaScript 写成的互动叙事游戏，关于大模型变成人的 16 章人间烟火；昼夜交替、好感度系统、仙剑式探索地图、结局图鉴。

这里有**千节点 Raft 分布式 KV 存储**、**LoRA 微调与 DPO 对齐**、**助手与智能体（DeepSeek·CAMEL）**、以及**大模型与计算机科学技术笔记**（6 份核心知识库）。

---

## 🧭 目录结构

```
Project of ChenShen/
├── LLM推理优化/                 # ★ 从零实现的推理优化工具链
│   ├── gpt.py · quantize.py · speculative.py · continuous.py
│   ├── benchmark.py            # 可复现基准
│   └── reports/                # 曲线图 + 综合报告
│
├── GPU System/                  # ★ GPU 能耗感知运行时（GEAR）
│   ├── software/                # DVFS + 功耗封顶 + 热管理 + ML 调频
│   ├── scripts/                 # calibrate / benchmark / estimate_cost
│   └── tests/ · archive/
│
├── Transformer与训练（从零实现）/  # train.py / generate.py / models/ / Dockerfile
│
├── 千节点Raft架构方案/           # ★ 分布式 KV（Go，Multi-Raft + etcd，1000 节点）
├── Raft分布式共识引擎/           # C++17 + standalone Asio 从零实现的 Raft + KV
│
├── 量化策略（聚宽·回测）/
│   ├── quant_v14.py            # ✅ 本地可跑：多资产风险平价
│   ├── joinquant_v18 · quant_v21 · quant_xgboost_shap  # 聚宽策略
│   ├── quant_features.py · 金融数学.py
│   └── README.md
│
├── 助手与智能体（DeepSeek·CAMEL）/
│   ├── src/dsh_assistant/      # ★ Python 包：config/llm/tts/memory/camel/assistant/cli
│   ├── tests/ · docs/ · examples/
│   └── README.md               # 统一 CLI：dsh-assistant voice|camel
│
├── 陈深的世界/                   # ★ 互动叙事游戏（典藏版）
│   ├── game/                   # index.html 主菜单 / world.html / story.html
│   ├── README.md · README.en.md
│   └── ScreenShot_*.png
│
├── 大模型与计算机科学技术笔记/   # ★ 6 份核心笔记 + README 索引
├── Python全章节学习笔记/
├── 机器学习作业/
├── LoRA领域大模型微调与对齐/     # LoRA + DPO 单卡微调
├── 量子纠错解码（Ising Decoding）/
├── web（工具·科普·校园·量化·生活）/
├── 其他工具（诗词·物理）/
│
├── tests/ · docs/
├── pyproject.toml · requirements.txt
├── .github/workflows/ci.yml
└── LICENSE                     # MIT
```

---

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 训练字符级 Transformer
python Transformer与训练（从零实现）/train.py --config Transformer与训练（从零实现）/config.yaml

# 推理优化 benchmark（KV Cache / 量化 / Continuous Batching）
python LLM推理优化/benchmark.py
python LLM推理优化/quant_compare.py
python LLM推理优化/cont_bench.py

# GPU 能效运行时（GEAR）
python GPU System/software/main.py --simulate --mode optimal

# 本地回测量化策略
python 量化策略（聚宽·回测）/quant_v14.py

# 助手与智能体（需要 DeepSeek API Key）
pip install -e "助手与智能体（DeepSeek·CAMEL）"
dsh-assistant voice

# 打开《陈深的故事》
start 陈深的世界/game/index.html
```

---

## ✨ 亮点

### 推理优化：核心亮点

| 层面 | 做法 | 关键结果 |
|------|------|----------|
| 解码复杂度 | KV Cache + prefill/decode | O(T²)→O(T)，实测 ~3.6× |
| 权重精度 | INT8/INT4/FP8 量化 | 存储压缩 4–5×，PPL 几乎无损 |
| 采样算法 | 投机解码 | target 前向降到 0.2 次/token |
| 服务吞吐 | Continuous Batching | 吞吐随 batch 近线性增长 |

### GPU 能效运行时（GEAR）

能耗感知 DVFS + 功耗封顶 + 温度保护，目标在不损失吞吐的前提下最小化能耗（训练预算上可省 20–30%，例如 DeepSeek-V3 的 $5.6M 成本）。含 ML 能效预测、可回收废热度量、训练成本估算（`estimate_cost.py`）。

### 分布式系统：两个 Raft

从共识协议到千节点存储，用 Go 与 C++17 各写一遍 Raft。C++ 版从零实现选举/日志复制/持久化/KV 状态机；Go 版放大到 etcd + Multi-Raft 千节点生产架构。

### 助手与智能体（DeepSeek·CAMEL）

标准 Python 包 + 统一 CLI：语音助手（DeepSeek + Edge TTS）与 CAMEL 角色化对话；`.env` 安全配置、超时+重试、线程安全原子写、12 单测、CI、完整文档。

---

## 📚 技术笔记

`大模型与计算机科学技术笔记/` 收录 6 份核心笔记（详见该目录 [README](大模型与计算机科学技术笔记/README.md)）：`大模型科学与工程`、`大模型全栈工程手册07201版`、`计算机科学与技术`、`LLM技术栈`、`贵系`、`量化`。

---

## 🛠 工程设施

```bash
pip install -e .[dev]          # pytest / ruff / mypy
pytest                         # 单元测试
ruff check tests "量化策略（聚宽·回测）/quant_features.py" LLM推理优化
```

- GitHub Actions CI：自动 lint + 单测 + 编译冒烟
- `.editorconfig` / `.pre-commit-config.yaml`
- Docker / docker-compose 支持

---

## 🗺 Roadmap

- [x] KV Cache → 量化 → 投机解码 → Continuous Batching
- [x] PagedAttention（分页 KV 缓存）
- [x] 千节点 Raft 分布式 KV 存储
- [x] GPU 能效运行时（GEAR）
- [x] 助手与智能体工程化（CLI 包 + 测试 + CI + 文档）
- [ ] 真·多机分布式推理
- [ ] 量化策略统一工程化 + 实盘风控
- [ ] 《陈深的故事》更多结局与章节

---

## License

[MIT](LICENSE) © 2026 · 个人学习与实验用途

---

> 如果这个仓库曾让你在某个深夜停下过一秒钟，那就是它存在的意义。
