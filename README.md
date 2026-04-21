# Project1
- 清华大学驭风计划NLP算法工程师研修班
- 全国中学生物理竞赛省级赛区一等奖
- 在手搓我的第一个Transformer+MOE混合模型
- 开发了基于随机森林的量化交易策略、风控AI智能化模型部署、及语音智能助手

- 本项目尝试构建一个 Mixture of Experts (MoE) 风格的私有AI系统。
- 核心思想：与其用一个庞大模型解决所有问题，不如训练多个小型、专业的“专家模型”，并由一个“路由器”根据任务类型，将请求路由给最合适的专家。

🏗️ 系统架构

模块	职责	 状态
物理专家	理解物理概念、公式推导、宇宙学与量子力学问答	🔄 训练中
翻译专家	中-英、英-中专业文献/技术文档翻译	🔄 数据准备
CFA金融专家	公司财务、估值、资产定价、ESG分析	🔄 训练中
量化基金专家	量化策略、因子投资、风险模型、代码生成	🟢 原型完成
计算机专家	系统设计、算法、编程语言、AI原理	🔄 训练中
轻量级路由器	意图识别与任务路由	📝 设计中

📂 项目文件说明
文件	描述	核心技术
joinquantV18.py	量化策略V18：基于随机森林的A股交易策略，集成滚动训练、动态风控	sklearn, 聚宽
模型全功能部署.py	全能AI工具包：从零实现的字符级Transformer，支持训练、生成、分类、RAG、INT8量化、Streamlit监控	PyTorch, Transformer, RAG, Streamlit
模型框架.py	优化版生成模型：解决“胡言乱语”，实现Top-K/P、重复惩罚、温度调节	PyTorch, 改进版Transformer
清华二校门智能语音助手小DeepSeek.py	带记忆的语音助手：基于DeepSeek API + Edge TTS，支持上下文对话与唤醒	OpenAI API, edge_tts
training_data.txt	训练语料库（自动生成）	从贵系.docx等提取
best_model.pth	当前最佳模型权重	持续迭代中
vocab.json	字符级词汇表	训练基础

1. 环境准备
bash
# 克隆仓库
git clone https://github.com/380992846-tech/Project1.git
cd Project1

# 安装核心依赖
pip install torch numpy scikit-learn pandas
pip install streamlit sentence-transformers  # 用于监控和RAG
# 可选：pip install python-docx edge-tts openai
2. 训练主模型
bash
# 基于《贵系》、《量化》、《宇宙》等文档训练字符级Transformer
python 模型框架.py --mode train
3. 使用量化策略（聚宽平台）
将 joinquantV18.py 代码复制到聚宽研究环境

运行回测，对比基准（沪深300）

4. 启动交互式AI工具包
bash
# 训练后，进入交互生成模式
python 模型全功能部署.py --mode generate

# 或启动监控仪表盘
python 模型全功能部署.py --mode dashboard
5. 运行语音助手
bash
# 配置DeepSeek API Key后运行
python 清华二校门智能语音助手小DeepSeek.py
📊 当前进展
✅ 字符级Transformer：从零实现，支持完整的训练、验证、生成流程

✅ 生成质量优化：实现Top-K、Top-P、重复惩罚、温度调节

✅ 量化交易基线：随机森林策略，年化收益跑赢基准

✅ 模型量化：INT8量化支持，2-3倍推理加速

🔄 MoE架构：5个专家模型 + 路由器的设计与训练

数据准备中：物理/CFA/计算机领域语料

训练进行中：使用云端GPU（A100）

原型已就绪：量化专家与翻译专家

🧠 技术栈
深度学习：PyTorch, Transformer, RAG

机器学习：Scikit-learn, XGBoost, 随机森林

量化金融：聚宽, NumPy, Pandas

部署优化：INT8量化, ONNX, Streamlit

应用：OpenAI API, Edge TTS

📈 训练监控
启动Streamlit仪表盘后，可实时监控：

训练/验证损失曲线

模型大小与推理速度

在线生成与参数调节

bash
streamlit run dashboard.py
🤝 贡献与交流
欢迎通过Issue交流技术问题

本项目的核心是自学与探索，所有代码均为独立实现

📜 许可证
MIT

最后
“读博不是学习，是贡献” —— 希望通过这个项目，积累从0到1构建专业AI系统的经验，为未来的博士研究打下基础。路还很长，但每一步都算数。
