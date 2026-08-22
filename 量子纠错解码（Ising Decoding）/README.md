# 量子纠错解码（Ising Decoding）

> 用 NVIDIA 的 **Ising Decoding**（AI 量子纠错预解码器）做**实时量子纠错**，目标：激活因缺乏快速解码器而被"雪藏"的**三角形颜色代码（Triangular Color Code）**。
>
> 从复现官方基准（对比 pyMatching）到硬件集成（延迟预算权衡），再到探索性微调，逐步推进实时量子纠错的工程化。

---

## 背景与动机

**量子比特极其脆弱**，纠错是迈向实用化必须攻克的难关。但传统解码算法（如匹配算法）速度跟不上实时需求。

**Ising Decoding** 是 NVIDIA 开源的一系列基于 **3D 卷积神经网络**的**预解码器**，专门用来加速这一过程。官方数据显示：在特定颜色代码和噪声模型下，可将逻辑错误率降低超过 **300 倍**（官方实测 **347×**）。

**本项目切入点**：针对**三角形颜色代码**训练一个轻量级 AI 预解码器——这是一种公认高效、但因缺乏快速解码器而被"雪藏"的纠错方案。目标是重新激活它，并量化相对传统解码器的性能提升。

---

## 相关资源（真实开源项目）

| 资源 | 说明 |
|------|------|
| [NVIDIA/ising-decoding](https://github.com/NVIDIA/ising-decoding) | 训练 recipes 仓库 |
| [NVIDIA/Ising](https://github.com/NVIDIA/Ising) | Ising 模型家族仓库 |
| [Ising-Decoder-ColorCode-1-Fast](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | 官方预训练颜色代码解码器（速度优化版） |
| [NVIDIA Ising 官方页](https://developer.nvidia.com/ising) | 官方产品介绍 |
| [Quantum Computing Report: 347×](https://quantumcomputingreport.com/nvidia-launches-open-ising-decoder-architecture-to-suppress-quantum-color-code-error-rates-by-347x/) | 官方 347× 错误率抑制报告 |

---

## 目录结构

```
量子纠错解码（Ising Decoding）/
├── README.md              # 本文件（研究计划 + 路线图）
├── docs/                  # 技术笔记、调研、benchmark 报告
├── data/                  # 训练数据、噪声模型配置
├── models/                # 下载/训练的预解码器权重
├── scripts/               # 训练 / 推理 / 对比脚本
└── results/               # 输出结果（json + 图表 + 报告）
```

---

## 三阶段研究路线图

### 第一阶段：复现与基准测试

**目标**：在标准噪声模型下，复现 Ising 对颜色代码的解码，对比行业标准 **pyMatching**。

- [ ] 跑通官方 Ising 训练脚本，生成针对**三角形颜色代码**的训练数据；
- [ ] 实现性能对比脚本 `scripts/quantum_bench.py`（参考 `LLM推理优化/benchmark.py` 的结构），
      把"对比 pyMatching"当成另一种"量化对比"；
- [ ] 量化提升：
  - **速度**：目标 ≥ 2.5×；
  - **精度**：目标 ≥ 3×（逻辑错误率降低）。

**与现有技能对接**：复用 `LLM推理优化/` 的 benchmark 方法论。

### 第二阶段：硬核系统集成

**目标**：将预解码器嵌入一个模拟的**量子控制环路**，研究**延迟预算**下的权衡。

- [ ] 新建 `quantum_control/` 目录（或复用 `千节点Raft架构方案/` 的 C++/Go 高性能经验），
      写一个模拟解码服务；
- [ ] 对比**速度优化版（0.9M 参数）**和**精度优化版（1.8M 参数）**
      在不同延迟要求（如 <1ms, <10ms）下的表现；
- [ ] 复用 `LLM推理优化/serving.py` 的批量推理服务经验，
      用 `continuous.py` 的思路处理并发解码请求。

**延迟预算**：系统容许的解码最大耗时。在预算约束下，权衡速度与精度。

### 第三阶段：探索性研究（可选）

**目标**：针对特定硬件架构或操作进行微调。

- [ ] 修改 Ising 的数据生成器，加入**超导噪声模型**的特性（如 T1/T2 退相干）；
- [ ] 针对特定硬件（超导 / 离子阱）微调 Ising Calibration；
- [ ] 探索预解码器与 **CUDA-Q** 平台的混合量子-经典实时控制框架；
- [ ] 探索颜色代码在**晶格手术（Lattice Surgery）**等更复杂逻辑操作中的应用。

---

## 关键概念

- **颜色代码（Color Code）**：一种量子纠错码，高效但历史上缺乏快速解码器；
- **三角形颜色代码（Triangular Color Code）**：本项目重点目标；
- **Ising Decoding**：基于 3D CNN 的预解码器，加速量子纠错；
- **pyMatching**：行业标准的匹配解码器（对比基线）；
- **逻辑错误率（Logical Error Rate）**：衡量纠错效果的核心指标。

---

## 环境与依赖

> 具体安装步骤需参考 [NVIDIA/ising-decoding](https://github.com/NVIDIA/ising-decoding) 官方 README（依赖 CUDA/PyTorch、stim、pyMatching 等）。本项目将在 `docs/` 中记录实际可复现的环境配置。

```bash
# 规划中的关键依赖（以官方仓库为准）
# - CUDA + PyTorch
# - stim（量子电路模拟）
# - pymatching（对比基线）
# - NVIDIA ising-decoding（官方 recipes）
```

---

## Roadmap

- [ ] 第一阶段：复现 + 对比 pyMatching（速度 ≥2.5× / 精度 ≥3×）
- [ ] 第二阶段：解码服务 + 延迟预算权衡（0.9M vs 1.8M 参数）
- [ ] 第三阶段：硬件微调 / CUDA-Q 集成 / 晶格手术（探索性）
- [ ] 全程：以 `docs/` 沉淀可复现的实验记录

---

> 这个项目的意义：不只是做一个项目，而是踏进量子计算最核心的工程前线——用 AI 基础设施能力，复活"颜色代码"。
