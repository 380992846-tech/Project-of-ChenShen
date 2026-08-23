# 从零实现的大模型推理优化 · 分布式系统 · 量化交易 · 创意工坊

—— 清华大学计算机科学与技术系

---

## 📖 关于这个仓库

这里有从零手搓的 decoder-only GPT，有 KV Cache、INT8/INT4 量化、投机解码、Continuous Batching——每一行代码都有可复现的 benchmark 和单元测试。

这里有量化交易策略，用随机森林、XGBoost+SHAP 在聚宽平台上跑回测，有动态风控、多资产风险平价。

这里有《陈深的故事》——一个用 HTML/CSS/JavaScript 写成的互动叙事游戏，关于大模型变成人的 16 章人间烟火。昼夜交替、好感度系统、仙剑式探索地图、结局图鉴……是代码写给算法的一封情书。

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
├── 千节点Raft架构方案/           # ★ 分布式 KV（Multi-Raft + etcd，Go，1000 节点）
│   ├── pkg/                     # metadata / raft / router / client / metrics
│   ├── cmd/                     # kvstore-node / router / client 入口
│   ├── scripts/                 # 集群启动 / 冒烟测试 / 性能基准
│   ├── docs/                    # etcd 部署详解
│   └── go.mod / Dockerfile* / docker-compose.yml
│
├── Raft分布式共识引擎/           # C++17 + standalone Asio 从零实现
│   ├── include/raft.h           # RaftNode 声明 + RPC/日志/持久化结构
│   ├── src/raft.cpp             # RPC 网络层 + KV 状态机 + main
│   ├── src/raft_node.cpp        # 选举 / 日志复制 / 持久化实现
│   ├── CMakeLists.txt           # FetchContent 自动拉取 Asio + nlohmann-json
│   └── test_cluster.sh / test_kv.sh / test_failover.sh
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
├── 大模型与计算机科学技术笔记/   # LLM技术栈 / 大模型工程 / 计算机科学 / 培养方案
├── Python全章节学习笔记/         # Python 语法 → 数据分析 → 算法 一站式笔记
├── 机器学习作业/                # 分类 · 聚类 · 集成 · 流失预测
├── LoRA领域大模型微调与对齐/    # LLaMA-2 LoRA + DPO
├── 量子纠错解码（Ising Decoding）/ # ★ AI 量子纠错预解码器（NVIDIA Ising，激活颜色代码）
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

## 分布式系统：两个 Raft

从共识协议到千节点存储，用两种语言各写一遍 Raft，理解分布式一致性的从零到一。

### 千节点 Raft 架构方案（Go · 生产级 Multi-Raft）

经过生产验证（TiKV / CockroachDB）的成熟架构，目标支撑 1000+ 节点、百万级 QPS 的分布式 KV 存储。

```
千节点分布式 KV 存储系统
├── 元数据集群 (etcd/Raft, 5节点)     # 管理分片映射、节点状态
├── 数据集群 (Multi-Raft, 200分片 × 5节点 = 1000节点)
├── 路由层 (无状态网关)               # key → 分片 → Leader
└── 客户端 SDK (路由缓存 + 失效重试)
```

| 模块 | 作用 |
|------|------|
| `pkg/metadata` | etcd 拓扑管理：分片映射、Leader 状态、watch 实时同步 |
| `pkg/raft` | 单分片 5 节点 Raft（KV 状态机 + 快照 + Join/Bootstrap） |
| `pkg/router` | 无状态路由网关，key → 分片 Leader 转发 |
| `pkg/client` | 客户端 SDK：路由缓存（TTL）+ 失效自动重定向 |
| `pkg/metrics` | Prometheus 指标（操作计数 / 延迟 / Raft 状态） |

- **架构**：etcd 元数据集群 + Multi-Raft 数据集群 + 无状态路由层 + 客户端路由缓存；
- **分片**：key 空间按范围分 200 片，每片 5 节点独立 Raft，故障隔离、线性扩展；
- **部署**：`scripts/start-cluster.sh` 一键起 1000 节点；`docker-compose.yml` + Prometheus/Grafana 监控；
- **文档**：`docs/etcd-cluster.md` 详解元数据集群部署与运维。

### Raft 分布式共识引擎（C++17 · 从零实现）

用 C++17 + standalone Asio（零 Boost 依赖）从零实现 Raft 协议，并在此基础上做了可交互的 KV 存储。

| 模块 | 实现 |
|------|------|
| **领导人选举** | 随机超时（500–1000ms）+ `RequestVote` + 选举限制（Log Matching Property） |
| **日志复制** | `AppendEntries` + 一致性检查（term + prevLogIndex）+ 冲突条目回退 |
| **持久化** | term / votedFor / 日志元数据落盘到 `raft_<id>.json`，重启恢复 |
| **KV 状态机** | `apply_command` 把已提交日志应用到 KV store（set/del），交互命令行 |

- **网络**：standalone Asio 异步 RPC，JSON 编解码，4 字节长度前缀帧格式；
- **线程模型**：单 io 线程处理 Raft 状态 + 命令行线程 `state_mutex_` 串行化，锁序统一 state→kv，无死锁；
- **故障转移**：kill Leader 后剩余节点自动重选（实测通过）；
- **验证**：`test_cluster.sh`（选举）、`test_kv.sh`（选举 + 故障转移）、`test_failover.sh`（Leader 崩溃重选）；
- **已知限制**：无快照、读为本地读（最终一致）、无 CheckQuorum、persist 无 fsync——均已标注在项目 README。

> 两套实现互为印证：C++ 版把共识协议从零写透，Go 版把它放大到千节点生产架构。

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
open 陈深的世界/陈深的故事V6.html
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

## 大模型与计算机科学技术笔记

精选知识库：从 LLM 前置到大模型工程，从计算机科学基础到量化与培养方案，去重后保留的 6 份核心笔记。

| 文件 | 内容 |
|------|------|
| `大模型科学与工程.md` | 大模型原理与工程实践（最全面） |
| `大模型全栈工程手册.md` | 大模型工程化全流程手册 |
| `计算机科学与技术.md` | 计算机科学基础（计算理论 / 体系结构） |
| `LLM技术栈.md` | LLM 前置知识：线性代数、概率论、信息论 |
| `量化.md` | 量化交易笔记 |
| `贵系.md` | 清华计算机系课程与培养 |

---

## Python 全章节学习笔记

`Python全章节学习笔记/` 从语法到算法的一站式 Python 笔记，覆盖笔试面试高频考点。

| 模块 | 内容 |
|------|------|
| **语法** | 数字、字符串、列表、字典、集合、深浅拷贝 |
| **函数式** | 匿名函数、递归、闭包、装饰器、生成器 |
| **常用模块** | random、collections、时间 |
| **文件与数据** | CSV、Excel、JSON、INI、OS |
| **进阶** | 正则表达式、异常处理、面向对象（继承/反射）、并发（多进程/多线程） |
| **工程** | MySQL 数据库、数据分析（NumPy、Matplotlib） |
| **算法** | 递归、回溯、动态规划、贪心、分治 |

- 主笔记：`Python全章节学习笔记/Python全章节学习笔记.md`
- 快速入口：`Python全章节学习笔记/README.md`

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
