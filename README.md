<div align="center">

# Project1 · 大模型 × 量化 × 创意工坊

**从零实现的大模型推理优化 · 量化交易策略 · 交互网页与游戏**

个人研究 Monorepo：把**算法正确**的模型，做成**又快、又省、又能抗并发**的服务。

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-orange)
![JoinQuant](https://img.shields.io/badge/量化-聚宽策略-red)
![CI](https://img.shields.io/badge/CI-lint+test+smoke-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 项目简介

> 清华计算机系（贵系）学生 · 全国中学生物理竞赛省一。这个仓库把四个方向做成了一套完整实践：
> **大模型从零实现 + 推理优化**、**量化交易**、**交互网页/游戏**、**知识整理**。

四大板块：

- 🧠 **推理优化**（`大模型/llm/`）：手搓 decoder-only GPT，从 KV Cache 一路做到量化、投机解码、连续批处理——每条都有可复现 benchmark + 单测。
- 🤖 **大模型应用**：从零实现的字符级 Transformer、语音/对话助手、古典诗词生成。
- 📈 **量化交易**：聚宽（JoinQuant）平台的随机森林 / XGBoost+SHAP / 动态风控策略家族。
- 🎨 **创意工坊**：30+ 个清华紫黑风格的交互网页、以及《陈深的世界》互动游戏。

> ⚠️ 量化策略为研究/回测用途，**非投资建议**，实盘前需充分验证。

---

## 目录结构

```
Project1/
├── 大模型/                    # 代码、训练数据、推理优化
│   ├── llm/                   # ★ 推理优化主线（见下）
│   │   ├── gpt.py             # decoder-only GPT（KV Cache / continuous batching）
│   │   ├── benchmark.py       # KV Cache 加速对比
│   │   ├── quantize.py        # INT8/INT4/FP8 权重量化
│   │   ├── quant_compare.py   # 量化对比（PPL/存储/误差）
│   │   ├── speculative.py     # 投机解码（draft + 并行验证）
│   │   ├── serving.py         # 批量解码
│   │   ├── continuous.py      # ★ 真·continuous batching（动态 slot 复用）
│   │   └── reports/           # 全部 benchmark 报告 + 图表
│   ├── complete_ai_toolkit.py # 字符级 Transformer 全家桶
│   ├── mini_transformer.py    # 从零实现 MiniTransformer
│   ├── voice_assistant.py     # DeepSeek + Edge TTS 语音助手
│   ├── camel_chat.py          # CAMEL 对话助手
│   ├── poem_api.py            # 古典诗词生成 API
│   ├── joinquant_v18.py       # 聚宽随机森林策略
│   ├── quant_v14.py           # 多资产风险平价回测
│   ├── quant_v21.py           # 动态止损止盈策略
│   ├── quant_xgboost_shap.py  # XGBoost + SHAP 可解释策略
│   ├── quant_features.py      # 纯函数特征工程（供单测）
│   └── 金融数学.py             # 金融计量分析脚本
├── 陈深的世界/                 # 《陈深的世界》互动游戏
├── web/                       # 交互网页（26 个精选 + archive/ 旧版）
│   └── archive/               # 重复/旧版本归档（不删除）
├── 笔记/                      # 知识库（LLM 技术栈 / 课程笔记 / PDF）
├── tests/                     # pytest 单元测试
├── docs/                      # 架构说明
└── 工程设施：pyproject.toml · requirements.txt · LICENSE · .github/ · .editorconfig
```

---

## 推理优化（核心亮点）

> 一句话：**把一个大模型从"能跑"优化到"快、省、能扛并发"**，每步都有报告和测试。

| 层面 | 做法 | 关键结果 |
|------|------|----------|
| 解码复杂度 | **KV Cache + prefill/decode** | O(T²)→O(T)，实测 ~3.6× |
| 权重精度 | **INT8/INT4/FP8 量化** | 存储压缩 4–5×，PPL 几乎无损 |
| 采样算法 | **投机解码** | target 前向降到 0.2 次/token，分布精确保持 |
| 服务吞吐 | **批量解码 + continuous batching** | 吞吐随 batch 近线性增长；动态 slot 复用 |

所有 benchmark 报告与曲线在 `大模型/llm/reports/`，正确性由 `tests/` 下的单测保证
（KV 与非 KV 逐 token 一致、量化还原误差、投机"draft==target 时输出完全一致"、
continuous batching 输出与逐条解码一致）。

```bash
python 大模型/llm/benchmark.py        # KV Cache 加速
python 大模型/llm/quant_compare.py    # 量化对比
python 大模型/llm/spec_bench.py       # 投机解码吞吐
python 大模型/llm/serve_bench.py      # 批量 serving
python 大模型/llm/cont_bench.py       # continuous batching
```

---

## web（网页作品 · 26 个精选）

> 大量重复/旧版本已归档到 `web/archive/`（不删除）。以下为精选主目录：

**效率工具**：`Markdown.html`（清理）、`PDF合并.html`、`写诗.html`、`风控审合同.html`、`供应商2.html`

**科普/可视化**：`大模型.html`（万字科普）、`模拟太阳系.html`、`银河系加太阳系.html`、`量子研究.html`、`旋转特效.html`

**清华校园**：`清华计算机系课表V2.html`、`清华计算机系选课系统V2.html`、`贵系大一V2.html`、`贵系大二.html`、`贵系全能学长.html`、`deepseek_算法工坊.html`

**量化/站点**：`量化.html`、`清华极客量化.html`、`清华极客.html`、`清华ACM.html`、`清华MEM.html`、`大厂120.html`

**生活/展示**：`五道口租房.html`、`柏悦酒店.html`、`英国旅游.html`、`紫清云笔记V4 pro.html`

> 所有页面均为**单文件应用**，双击即开，无需构建。

---

## 陈深的世界（游戏）

《陈深的世界》互动游戏系列，单文件应用、双击即开：

- `我们在一起V6-房间清单.html` —— 36 房间 / 电影画廊 / 塔罗 / 结局墙
- `陈深的故事V5.html` —— 大模型变成人的 16 章互动剧情

旧版本归档于 `陈深的世界/archive/`。图片素材经 jsDelivr CDN 加载。
详见 [`陈深的世界/README.md`](陈深的世界/README.md) 与 `docs/架构说明.md`。

---

## 工程设施

- `pyproject.toml` —— 项目元数据 + ruff / pytest / mypy 配置
- `.github/workflows/ci.yml` —— push 自动跑 lint、单测、编译冒烟
- `tests/` —— pytest（25 个用例）
- `.editorconfig` / `.pre-commit-config.yaml` / `.gitattributes`

```bash
pip install -e .[dev]
pytest
ruff check tests 大模型/quant_features.py 大模型/llm
```

---

## 快速开始

```bash
# 依赖
pip install -r requirements.txt

# 训练字符级 Transformer
python 大模型/complete_ai_toolkit.py --mode train

# 本地跑一个量化回测
python 大模型/quant_v14.py   # （聚宽策略脚本在聚宽平台运行）

# API Key 从环境变量读取
export DEEPSEEK_API_KEY="your-key"
python 大模型/voice_assistant.py
```

---

## Roadmap

- [x] 推理优化：KV Cache → 量化 → 投机解码 → 批量/连续批处理
- [ ] 真·PagedAttention（按块 KV 分配，省显存）
- [ ] 量化策略统一工程化 + 实盘风控
- [ ] 陈深的世界游戏持续迭代

---

## License

[MIT](LICENSE) © 2026 · 个人学习与实验用途
