# Project1 · 个人 AI × 量化 × 创意工坊

> 一个集大模型实现、量化交易策略、物理模拟与网页应用于一体的个人学习与实验仓库。
> 作者：清华计算机系（贵系）学生 · 全国中学生物理竞赛省一

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-orange)
![JoinQuant](https://img.shields.io/badge/JoinQuant-聚宽策略-red)
![HTML](https://img.shields.io/badge/HTML-35个页面-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 项目简介

本仓库是作者在 **大模型（LLM）**、**量化交易（Quant）**、**物理模拟** 与 **Web 创意工具** 四个方向上的学习与实践合集：

- 🧠 **大模型从零实现**：不依赖现成框架地搭建 Transformer，理解注意力机制、生成策略、RAG 与量化；
- 📈 **量化交易策略家族**：基于聚宽（JoinQuant）平台的多版本策略迭代（V14 → V18 → V21），融合机器学习与情绪因子；
- 🎨 **创意 Web 应用**：30+ 个清华风格（黑紫玻璃）HTML 页面，覆盖课表、选课、笔记、面试题库与日常工具；
- 📚 **系统性知识库**：大模型、计算机科学与 LLM 技术栈的深度整理文档。

---

## 🗂️ 目录结构

```
Project1/
├── 🐍 Python 模块（11 个）
│   ├── complete_ai_toolkit.py             # 全功能 AI 工具包（见下方详解）
│   ├── transformer_O-O.py                 # 从零实现 MiniTransformer
│   ├── TSINGHUA-小DS.py                   # 清华二校门智能语音助手
│   ├── chat_with_jiujiu.py                # CAMEL × DeepSeek 对话助手
│   ├── Poem.py                            # PoeticFlow 古典诗词生成 API
│   ├── elastic_collision_sim.py           # 一维弹性碰撞物理模拟
│   ├── joinquantV18.py                    # 聚宽 A股策略（随机森林版）
│   ├── V14.py                             # 多资产风险平价量化系统
│   ├── V21quant Model.py                  # 聚宽 ETF 交易策略（V21）
│   ├── SHAP+值增量学习+LSTM+XGBoost.py     # 可解释 AI 选股策略
│   └── 金融数学                            # 金融计量分析脚本
├── 🖥️ HTML 应用（35 个）
│   ├── 校园课表/选课/叙事（6） 清华大学课程表、选课系统V2、贵系大一/大二…
│   ├── 学习笔记/工坊（5）     紫清云笔记（V1/V2/V4pro）、贵系全能学长、deepseek_算法工坊
│   ├── 面试题库（4）         大厂120、大厂助手、大厂面试、大厂面试笔记
│   ├── 效率工具（5）         Markdown清理器、PDF合并、风控审合同、写诗
│   ├── 科技可视化（4）       模拟太阳系、银河系+太阳系、量子研究、旋转特效
│   └── 科普/量化/站点/生活（11） 大模型科普、量化舱、清华极客、ACM/MEM、柏悦酒店、英国旅游、五道口租房…
├── 📚 知识库文档（4 本）
│   ├── 大模型科学与工程.md（172 KB）
│   ├── 计算机科学与技术.md（117 KB）
│   ├── LLM技术栈.md（43 KB）
│   └── 大模型全栈工程手册07201版.md（53 KB）
├── 📄 参考资料（PDF/DOCX）
│   ├── Large Language Model (LLM).pdf / 算力中心资产管理.pdf / 贵系培养方案.pdf
│   └── 量化.docx / 贵系.docx / 宇宙与物理规律.docx
└── 🗂️ 数据文件
    ├── training_data.txt     # LLM 训练语料（计算机科学知识文本）
    └── vocab.json            # 字符词表
```

---

## 🧠 Python 模块详解

### 1. `complete_ai_toolkit.py` — 全功能 AI 工具包 ⭐

一个文件整合完整 AI 流程：文档处理 → 训练 → 生成 → 问答 → 量化 → 可视化。

| 功能 | 命令 | 说明 |
|------|------|------|
| 文档处理 | `--mode build` | 读取 `.docx` / `.txt` 构建训练语料 |
| 训练 | `--mode train` | 字符级 `CharTransformer`（8头注意力×4层） |
| 分类 | `--mode classify` | 文本分类器（含主题向量） |
| 生成 | `--mode generate` | 条件文本生成（温度/重复惩罚控制） |
| RAG 问答 | `--mode rag` | `SimpleRAG`：索引检索 + 生成回答 |
| 量化加速 | `--mode quantize` | INT8 量化，2–3 倍推理加速 |
| 监控面板 | `--mode dashboard` | Streamlit 实时监控训练曲线与推理 |

### 2. `transformer_O-O.py` — 从零实现 MiniTransformer

- 完整 `MiniTransformer`：Embedding + 可学习位置编码 + `TransformerEncoder` + 线性输出头；
- 用**算术序列**（`[a, b, c] → [b, c, a+b]`）演示 next-token 预测；
- 工程细节：`AdamW` 优化器、`StepLR` 学习率衰减、CrossEntropyLoss。

### 3. `TSINGHUA-小DS.py` — 清华二校门智能语音助手

- 基于 **DeepSeek API + Edge TTS** 的语音对话助手；
- 特色：按时间智能问候、**对话记忆持久化**（JSON）、语音播放、角色化人设（"小DeepSeek"）。

### 4. `chat_with_jiujiu.py` — CAMEL 多智能体对话

- 基于 **CAMEL 框架** 的对话助手，接入 DeepSeek 模型平台，循环命令行交互。

### 5. `Poem.py` — PoeticFlow 古典诗词生成 API

- Flask RESTful 服务：词库（名词/动词/意象/情感）+ 格律校验 + 风格调制；
- 启动后访问 `http://localhost:5000`。

### 6. `elastic_collision_sim.py` — 弹性碰撞物理模拟

- **事件驱动引擎**：碰撞时刻预测、完全弹性碰撞解析、球-球/球-墙碰撞、重叠修复；
- 备选 **RK4 积分器** 路线，支持轨迹绘图、动画帧导出与质量比扫描实验。

### 7. `joinquantV18.py` — 聚宽 A股策略 v18

- 特征工程（RSI 等技术指标）→ **随机森林** 分类 → 滚动训练；
- 集成动态风控与回测对比模块（`backtest_compare`）。

### 8. `V14.py` — 多资产风险平价量化系统

- 多资产数据抓取（带本地缓存 `data_cache`）→ 特征标准化 → 随机森林信号；
- **风险平价** 权重分配 + RSI 择时，含完整回测与日志体系。

### 9. `V21quant Model.py` — 聚宽 ETF 交易策略 V21

- 交易标的：沪深300 ETF（510300）；
- 核心机制：**ATR 动态止损止盈**、RSI 背离、布林带因子、**分批止盈**、大盘环境过滤、波动率过滤、无进展止损。

### 10. `SHAP+值增量学习+LSTM+XGBoost.py` — 可解释 AI 选股策略

- 情绪因子：新闻 / 社交舆情情感打分；
- 模型融合：**LSTM + XGBoost** 双模型信号；
- 可解释性：**SHAP** 特征重要性报告；**值增量学习**：收益分歧检测 + 增量训练；
- 动态阈值：ATR + 市场状态（牛/熊/震荡）自适应。

### 11. `金融数学` — 金融计量分析脚本

- NumPy / Pandas / SciPy / ARCH 技术栈，含 GARCH 类波动率建模等计量分析。

---

## 🖥️ HTML 应用速览

| 分类 | 页面（共 35 个） | 说明 |
|------|-----------------|------|
| 校园课表/选课/叙事（6） | `清华大学课程表.html`、`清华计算机系课程表.html`/`V2`、`清华计算机系选课系统V2.html`、`贵系大一V2.html`、`贵系大二.html` | 清华黑紫风格课表、选课交互与角色化校园故事 |
| 学习笔记/工坊（5） | `紫清云笔记加强版.html`/`V2`/`V4 pro`、`贵系全能学长.html`、`deepseek_算法工坊.html` | 笔记工具三版本迭代 + AI 工具聚合页 |
| 面试题库（4） | `大厂120.html`、`大厂面试.html` | 大厂面试 120 题 |
| 效率工具（5） | `Markdown.html`、`PDF合并.html`、`风控审合同.html`、`供应商2.html`、`写诗.html` | Markdown 清理、PDF 合并、合同风控、诗词生成 |
| 科技可视化（4） | `模拟太阳系.html`、`银河系加太阳系.html`、`量子研究.html`、`清华大学计算机科学与技术系旋转特效.html` | 粒子/CSS 特效宇宙 |
| 知识科普（1） | `大模型.html` | 大模型万字科普页 |
| 量化主题（2） | `量化.html`（紫金投资舱）、`清华极客量化.html`（THU Quant） | 量化投资主题页 |
| 校园站点（3） | `清华极客.html`、`清华ACM.html`、`清华MEM.html` | 社团/培训/考研复习站 |
| 展示/生活（5） | `我们在一起V4.html`、`柏悦酒店.html`、`英国旅游.html`、`五道口租房.html`、`贵系学长.html.html` | 个人项目与生活展示 |

> 💡 所有 HTML 页面均为**单文件应用**，双击即可在浏览器打开，无需构建。

---

## 📚 知识库文档

| 文档 | 规模 | 内容 |
|------|------|------|
| `大模型科学与工程.md` | 172 KB | 从数学/算力基石到 Transformer、Scaling Laws、RLHF/DPO、分布式训练的体系化知识库 |
| `计算机科学与技术.md` | 117 KB | 数据结构、操作系统、数据库、分布式共识（Raft）等系统性梳理 |
| `LLM技术栈.md` | 43 KB | RFC 风格技术文档：自注意力从数学推导到 CUDA 实现、Flash Attention、Mamba 等 |
| `大模型全栈工程手册07201版.md` | 53 KB | 大模型工程实践手册（学术精修与系统重构版） |

---

## 🚀 快速开始

### 环境要求
- Python 3.9+
- 量化策略（`joinquantV18.py`、`V21quant Model.py`、`SHAP+值增量学习+LSTM+XGBoost.py`）需在**聚宽（JoinQuant）**平台运行

### AI 工具包
```bash
pip install torch streamlit python-docx

python complete_ai_toolkit.py --mode train        # 训练字符级 Transformer
python complete_ai_toolkit.py --mode generate     # 条件文本生成
python complete_ai_toolkit.py --mode rag          # RAG 问答
python complete_ai_toolkit.py --mode quantize     # INT8 量化
python complete_ai_toolkit.py --mode dashboard    # Streamlit 监控面板
```

### 诗词生成 API
```bash
pip install flask flask-cors numpy scikit-learn
python Poem.py
# 访问 http://localhost:5000
```

### 物理模拟
```bash
pip install numpy matplotlib
python elastic_collision_sim.py --balls 5 --tmax 20 --animate
```

### 语音助手 / 对话助手
```bash
pip install edge-tts openai camel-ai
# 1) 在 TSINGHUA-小DS.py / chat_with_jiujiu.py 中配置 DEEPSEEK_API_KEY
# 2) 运行脚本开始对话
```

---

## 🛠️ 技术栈

| 领域 | 技术 |
|------|------|
| 深度学习 | PyTorch、Transformer、RAG、MoE、INT8 量化、Streamlit |
| 机器学习 | Scikit-learn、XGBoost、LSTM、随机森林、SHAP |
| 量化金融 | 聚宽（JoinQuant）、风险平价、ATR/RSI/布林带、GARCH |
| 大模型应用 | DeepSeek API、OpenAI SDK、CAMEL、Edge TTS |
| 物理模拟 | 事件驱动仿真、RK4 数值积分、Matplotlib 动画 |
| Web 前端 | 原生 HTML/CSS/JS（单文件应用） |

---

## 🗺️ 项目进展与路线图

- [x] Transformer 从零实现（训练/验证/生成）
- [x] 生成质量优化（Top-K/P、重复惩罚、温度调节）
- [x] 量化交易基线（随机森林策略）
- [x] INT8 量化加速与 KV Cache 实践
- [x] MoE 架构原型（专家网络 + 路由机制）
- [x] RAG 检索增强问答
- [ ] 长上下文扩展（RoPE 插值）
- [ ] 多模态模型探索
- [ ] 策略实盘对接与组合风控

---

## ⚠️ 注意事项

1. **API Key**：`chat_with_jiujiu.py` 与 `TSINGHUA-小DS.py` 中的 `DEEPSEEK_API_KEY` 需自行填写，请勿提交真实密钥；
2. **量化策略**：聚宽策略为研究/回测用途，实盘前需充分验证与风控评估，本仓库不对投资结果负责；
3. **数据文件**：`training_data.txt` 为自整理训练语料，`vocab.json` 为配套词表。

---

## 📄 License

[MIT](LICENSE) © 2026 · 本项目为个人学习与实验用途，欢迎自由使用与改进。
