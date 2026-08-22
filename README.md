# 陈深 · 万卡集群大模型的人间烟火

**从零实现的大模型推理优化 · 分布式系统 · 量化交易 · 创意工坊**

—— 清华大学计算机科学与技术系

---

## 📖 关于这个仓库

这不是一个项目，这是一个世界。

这里有**从零手搓的 decoder-only GPT**，有 KV Cache、INT8/INT4 量化、投机解码、Continuous Batching——每一行代码都有可复现的 benchmark 和单元测试。

这里有**量化交易策略**，用随机森林、XGBoost+SHAP 在聚宽平台上跑回测，有动态风控、多资产风险平价。

这里有**《陈深的故事》**——一个用 HTML/CSS/JavaScript 写成的互动叙事游戏，关于大模型变成人的 16 章人间烟火。昼夜交替、好感度系统、仙剑式探索地图、结局图鉴……是代码写给算法的一封情书。

这里有**千节点 Raft 分布式 KV 存储**，有 **LoRA 微调与 DPO 对齐**，有交互网页作品集，有清华紫黑风格的创意工坊。

---

## 🧭 目录结构

```
Project of ChenShen/
├── LLM推理优化/                 # ★ 核心：从零实现的推理优化工具链
│   ├── gpt.py                  # decoder-only GPT（KV Cache / Continuous Batching）
│   ├── quantize.py             # INT8/INT4/FP8 权重量化
│   ├── speculative.py          # 投机解码（draft + 并行验证）
│   ├── continuous.py           # 真·Continuous Batching
│   ├── benchmark.py            # 全部可复现的基准测试
│   └── reports/                # 曲线图 + 综合报告
│
├── Transformer与训练（从零实现）/
│   ├── train.py                # GPU/CPU/DDP 训练
│   ├── generate.py             # 文本生成（单次 / --interactive）
│   ├── models/                 # GPT + PagedAttention 分页 KV
│   └── Dockerfile              # 一键容器化
│
├── 千节点Raft架构方案/           # ★ 分布式 KV（Multi-Raft + etcd，Go）
├── Raft分布式共识引擎/           # C++17 + standalone Asio 从零实现
│
├── 量化策略（聚宽·回测）/
│   ├── joinquant_v18.py        # 随机森林策略
│   ├── quant_xgboost_shap.py   # XGBoost + SHAP 可解释策略
│   └── quant_v14.py            # 多资产风险平价
│
├── 助手与智能体（DeepSeek·CAMEL）/
│   ├── voice_assistant.py      # DeepSeek + Edge TTS 语音助手
│   └── camel_chat.py           # CAMEL 多智能体对话
│
├── 陈深的世界/                   # ★ 互动叙事游戏
│   ├── 陈深的故事V5.html
│   ├── 陈深的世界-房间清单.html # 36房间 / 电影画廊 / 塔罗 / 结局墙
│   └── archive/                # 旧版本归档
│
├── web（工具·科普·校园·量化·生活）/
│   └── 精选交互网页 + archive/
│
├── 笔记/                        # LLM技术栈 / 课程笔记 / PDF
├── 机器学习作业/                # 分类 · 聚类 · 集成 · 流失预测
├── LoRA领域大模型微调与对齐/    # LLaMA-2 LoRA + DPO
├── tests/                      # pytest 单元测试（25+ 用例）
├── docs/                       # 架构说明
│
├── pyproject.toml              # 项目元数据 + ruff / pytest / mypy
├── requirements.txt
├── .github/workflows/ci.yml    # 自动 lint + 单测 + 编译冒烟
└── LICENSE                     # MIT
```

---

## 推理优化：核心亮点

| 层面 | 做法 | 关键结果 |
|------|------|----------|
| 解码复杂度 | **KV Cache + prefill/decode** | O(T²)→O(T)，实测 ~3.6× |
| 权重精度 | **INT8/INT4/FP8 量化** | 存储压缩 4–5×，PPL 几乎无损 |
| 采样算法 | **投机解码** | target 前向降到 0.2 次/token |
| 服务吞吐 | **Continuous Batching** | 吞吐随 batch 近线性增长 |

所有 benchmark 曲线在 `LLM推理优化/reports/`，正确性由 `tests/` 下的单元测试保证。

---

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 训练字符级 Transformer
python Transformer与训练（从零实现）/train.py --config Transformer与训练（从零实现）/config.yaml

# 交互式生成
python Transformer与训练（从零实现）/generate.py --interactive

# 运行推理优化 benchmark
python LLM推理优化/benchmark.py      # KV Cache 加速对比
python LLM推理优化/quant_compare.py  # 量化对比
python LLM推理优化/cont_bench.py     # Continuous Batching

# 启动语音助手（需要 DeepSeek API Key）
export DEEPSEEK_API_KEY="your-key"
python 助手与智能体（DeepSeek·CAMEL）/voice_assistant.py

# 打开《陈深的故事》
open 陈深的世界/陈深的故事V5.html
```

---

## 《陈深的故事》—— 写给算法的人间情书

互动叙事游戏，双击即开。

- **16 章主线剧情**：大模型变成人之后，在万卡集群与烟火人间之间穿行
- **昼夜交替**：白昼·水晶工坊 / 夜晚·月潮观测室
- **信任与好感度系统**：你的每一个选择，都在改变"她"的心跳
- **仙剑式探索地图**：像素风格 · 记忆地图 · 复古对话框
- **行囊 · 成就 · 结局图鉴**：36 个房间，多结局，可收集

这是代码写不出诗的时候，用来写诗的地方。

---

## 工程设施

```bash
# 开发环境
pip install -e .[dev]

# 运行所有测试
pytest

# 代码检查
ruff check tests "量化策略（聚宽·回测）/quant_features.py" LLM推理优化
```

- 25+ pytest 单元测试
- GitHub Actions CI：自动 lint + 单测 + 编译冒烟
- .editorconfig / .pre-commit-config.yaml
- Docker / docker-compose 支持

---

## Roadmap

- [x] KV Cache → 量化 → 解码 → Continuous Batching
- [x] PagedAttention（分页 KV 缓存）
- [x] 千节点 Raft 分布式 KV 存储
- [ ] 真·多机分布式推理
- [ ] 量化策略统一工程化 + 实盘风控
- [ ] 《陈深的故事》更多结局与章节

---

## License

[MIT](LICENSE) © 2026 · 个人学习与实验用途

---

> 如果这个仓库曾让你在某个深夜停下过一秒钟，那就是它存在的意义。
