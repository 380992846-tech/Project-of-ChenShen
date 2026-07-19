全国中学生物理竞赛省一

Project1: 全栈AI工作台与量化策略系统

https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/Python-3.8+-blue.svg

项目简介

本项目是一个集量化交易、大语言模型(LLM)训练与应用于一体的综合性工作台。它是我对AI系统从理论到实践的探索。

核心亮点：

· 量化策略：基于随机森林的A股交易策略，在聚宽平台回测跑赢沪深300基准。

· 从零实现LLM工具链：包含字符级Transformer的完整训练、生成、RAG及INT8量化工具包。

· MoE架构原型：设计并实践了包含5个专家模型与轻量级路由器的稀疏激活架构。

· 智能语音助手：基于DeepSeek API和Edge TTS，支持上下文对话和语音唤醒。

相关技术笔记:

· 大模型科学与工程知识库 - 涵盖Transformer、Scaling Laws、RLHF/DPO、分布式训练等核心理论。

· 计算机科学知识库 - 梳理了从计算理论、数据结构、操作系统到分布式共识（Raft）的系统性知识。


核心特性

模块 核心文件 描述 技术栈
核心量化策略 joinquantV18.py 基于随机森林的A股交易策略，集成滚动训练与动态风控。 sklearn, 聚宽

LLM全功能工具包 模型全功能部署.py 从零实现字符级Transformer，支持训练、生成、RAG、INT8量化、Streamlit监控。 PyTorch, Transformer, RAG

LLM生成优化 模型框架.py 实现了Top-K/P采样、重复惩罚与温度调节等生成控制。 PyTorch

智能语音助手 清华二校门智能语音助手小DeepSeek 基于DeepSeek API + Edge TTS，支持上下文对话与语音唤醒。 DeepSeek API, edge_tts

MoE架构探索 transformer_O-O.py 混合专家模型（MoE）原型，包含专家网络与路由机制设计。 PyTorch


🗂️ 项目文件结构

```text
.
├── README.md                   # 项目说明
├── 大模型科学与工程.md          # 大模型核心技术笔记
├── 计算机科学与技术.md          # 计算机科学系统性知识梳理
│
├── quant/                      # 量化交易模块
│   └── joinquantV18.py         # 聚宽量化策略
├── llm/                        # 大模型核心模块
│   ├── 模型全功能部署.py       # 从零实现Transformer工具包
│   ├── 模型框架.py             # 生成优化框架
│   ├── transformer_O-O.py      # MoE架构原型
│   ├── training_data.txt       # 训练语料库
│   ├── best_model.pth          # 最佳模型权重
│   └── vocab.json              # 字符级词汇表
├── assistant/                  # 智能助手模块
│   └── 清华二校门智能语音助手小DeepSeek
└── docs/                       # 其他文档与资源
    ├── Large Language Model (LLM).pdf
    └── ...
```

---

快速开始

环境安装

```bash
# 基础依赖
pip install torch numpy scikit-learn pandas

# 监控与RAG功能依赖
pip install streamlit sentence-transformers
```

运行量化策略（聚宽平台）

1. 将 quant/joinquantV18.py 中的代码复制到聚宽研究环境的策略编辑器中。
2. 设置回测参数（时间、频率、基准等）。
3. 运行回测，观察策略表现。

启动LLM训练监控面板

```bash
streamlit run llm/模型全功能部署.py
```

启动后，在浏览器中实时监控：

· 训练/验证损失曲线
· 模型大小与推理速度
· 在线生成与参数调节效果评价

项目进展 & 技术探索

Transformer从零实现：完整支持训练、验证与生成，并深入理解了Flash Attention、RoPE等底层原理。

生成质量优化：实现Top-K/P、重复惩罚、温度调节等采样策略。

量化交易基线：建立随机森林策略，年化收益跑赢基准。

模型量化与加速：支持INT8量化，实现2-3倍推理加速，并实践了KV Cache优化。

MoE架构原型：完成5个专家模型 + 路由器的设计与原型验证。

专家模型训练：基于整理的物理、CFA、计算机领域语料，进行正式训练。

长上下文扩展：探索RoPE插值技术，扩展模型上下文窗口。


🛠️ 技术栈

领域 技术

深度学习 PyTorch, Transformer, RAG, MoE

机器学习 Scikit-learn, XGBoost, 随机森林

量化金融 聚宽, NumPy, Pandas

部署与优化 INT8量化, ONNX, Streamlit, KV Cache

应用集成 OpenAI API, Edge TTS

相关资源

大模型科学与工程知识库 - 深入探讨了Transformer架构、Scaling Laws、RLHF/DPO、分布式训练（ZeRO）等核心话题。

计算机科学知识库 - 系统性梳理了从数据结构、操作系统、数据库到分布式共识（Raft）的核心知识点。

📄 许可证

本项目采用 MIT 许可证。
