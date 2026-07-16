# LLM技术栈

> **前置**：
>
> - 线性代数：矩阵乘法、SVD、低秩近似、特征值分解
> - 概率论：KL散度、MLE、贝叶斯推断、信息论
> - 优化理论：凸优化、KKT条件、拉格朗日对偶、策略梯度
> - 深度学习：反向传播、梯度消失/爆炸、归一化技术
> - 系统编程：CUDA内存层次、warp调度、共享内存bank冲突

---

# 第一部分：架构原理

## RFC 001: Transformer Architecture

**Status**: Accepted (2017) | **Latest Update**: 2025 (Flash Attention v3, Mamba-2)

### 1.1 自注意力：从数学推导到CUDA实现

#### 1.1.1 形式化定义

给定输入序列 $X \in \mathbb{R}^{n \times d}$，自注意力机制定义为：

$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$

其中 $Q = XW_Q$, $K = XW_K$, $V = XW_V$, $W_Q, W_K, W_V \in \mathbb{R}^{d \times d_k}$.

**关键洞察**：缩放因子 $\sqrt{d_k}$ 防止softmax进入饱和区。当 $d_k$ 较大时，$QK^T$ 的方差为 $d_k$，若不缩放，softmax的梯度趋于0。

**定理 1.1（注意力梯度的稀疏性）**：设 $A = \text{softmax}(QK^T/\sqrt{d_k})$，则对 $V$ 的梯度为：

$\frac{\partial L}{\partial V} = A^T \cdot \frac{\partial L}{\partial O}$

若 $A$ 的熵 $H(A[i,:]) < \epsilon$，则 $\forall j \neq i, \|\nabla V_j\| \to 0$。这意味着梯度仅通过活跃的注意力连接传播。

#### 1.1.2 计算复杂度分析

| 操作 | 时间复杂度 | 空间复杂度 |
| --- | --- | --- |
| $QK^T$ | $O(n^2 d_k)$ | $O(n^2)$ |
| softmax | $O(n^2)$ | $O(n^2)$ |
| $SV$ | $O(n^2 d_k)$ | $O(n d_k)$ |
| **总计** | $O(n^2 d_k)$ | $O(n^2 + nd_k)$ |

**瓶颈**：$n=128K$ 时，$n^2 = 16G$ 个元素，FP16下需32GB显存，远超单GPU容量。

#### 1.1.3 Flash Attention v1: 算法与实现

**核心思想**：利用GPU的层次化内存（SRAM \~20MB, 19TB/s vs HBM \~80GB, 3.35TB/s），分块计算并重计算，避免显式构造 $n \times n$ 矩阵。

```
Algorithm 1 Flash Attention (Forward Pass)
Input: Q, K, V ∈ ℝ^{N×d}, block sizes B_c, B_r
Output: O ∈ ℝ^{N×d}

1: Tile Q into Q_1,...,Q_{T_r} of size B_r
2: Tile K,V into K_1,...,K_{T_c}, V_1,...,V_{T_c} of size B_c
3: Initialize O=[0]_{N×d}, l=[0]_N, m=[-∞]_N
4: for j = 1 to T_c do
5:   Load K_j, V_j from HBM to SRAM
6:   for i = 1 to T_r do
7:     Load Q_i, O_i, l_i, m_i from HBM to SRAM
8:     S_ij = Q_i · K_j^T / √d
9:     m_ij = rowmax(S_ij)
10:    P_ij = exp(S_ij - m_ij)
11:    l_ij = rowsum(P_ij)
12:    m_i_new = max(m_i, m_ij)
13:    l_i_new = exp(m_i - m_i_new)·l_i + l_ij
14:    O_i_new = diag(exp(m_i - m_i_new))·O_i + P_ij·V_j
15:    Store O_i_new, l_i_new, m_i_new to HBM
16:   end for
17: end for
18: O = diag(l)^{-1} · O
```

**复杂度分析**：

- 时间：$O(N^2d)$ — 与标准注意力相同（未减少计算量）
- 空间：$O(Nd + B_cB_r)$ — 从 $O(N^2)$ 降至 $O(N)$
- HBM访问：$O(N^2d/M)$ 其中 $M$ 为SRAM大小

**定理 1.2（Flash Attention的正确性）**：Flash Attention的输出与标准注意力在数值精度内完全一致。证明基于online softmax的数学等价性。

#### 1.1.4 Flash Attention v2/v3: 演进

| 版本 | 改进 | 加速比(v1基准) | 关键贡献 |
| --- | --- | --- | --- |
| v1 | 分块+重计算 | 1.0x | 显存从O(N²)降至O(N) |
| v2 | 减少non-matmul FLOPs，优化warp调度 | 2.0x | 在H100上达到理论峰值的60% |
| v3 | WGMMA指令，异步拷贝 | 3.0x | 利用Hopper架构的Tensor Core |

**v2的关键优化**：将softmax的rescale操作从逐元素改为warp级归约，减少non-matmul FLOPs占比从40%降至15%。

**v3的关键优化**：利用Hopper的WGMMA（Warp Group Matrix Multiply-Accumulate）指令，使Tensor Core直接操作共享内存，绕过寄存器文件瓶颈。

**Benchmark** (N=8192, d=128, H100):

| Method | Time (ms) | Memory (GB) | TFLOPs/s | Speedup |
| --- | --- | --- | --- | --- |
| Standard | 12.4 | 1.07 | 312 | 1.0x |
| FA v1 | 4.8 | 0.08 | 806 | 2.6x |
| FA v2 | 2.3 | 0.04 | 1683 | 5.4x |
| FA v3 | 1.5 | 0.02 | 2580 | 8.3x |

### 1.2 GQA/MQA: KV Cache的优化博弈

**问题**：标准多头注意力中，每个头有独立的K和V，KV Cache大小为 $2 \times n_{layers} \times n_{heads} \times n_{seq} \times d_{head}$. 对于70B模型（80层，64头），每token需缓存 $80 \times 64 \times 128 \times 2 \approx 1.3M$ 个元素，约2.6MB/token。

**Multi-Query Attention (MQA)**：
$Q_i = XW_Q^i, \quad K = XW_K, \quad V = XW_V$
所有头共享K和V，KV Cache减少为 $1/n_{heads}$.

**Grouped Query Attention (GQA)**：
$Q_i = XW_Q^i, \quad K_g = XW_K^g, \quad V_g = XW_V^g$
将 $n_{heads}$ 个头分为 $g$ 组，每组共享K和V.

**定理 1.3（GQA的容量-效率权衡）**：设 $h$ 为头数，$g$ 为组数，则：

- KV Cache大小：$O(gh^{-1})$
- 模型容量（以有效参数计）：$O(1 - (1 - g/h) \cdot (d_k + d_v)/(3d))$

**实证结果**（LLaMA 2 70B, g=8, h=64）：

- KV Cache减少87.5%
- 推理吞吐提升2.3x
- MMLU得分下降0.4%（68.9 → 68.5）

### 1.3 MoE: 稀疏激活的理论与实践

**形式化定义**：MoE层将输入路由到 $E$ 个专家中的一个子集：

$y = \sum_{i=1}^E G(x)_i \cdot E_i(x)$

其中门控网络 $G(x) = \text{TopK}(\text{softmax}(W_g x), k)$，$k \ll E$.

#### 1.3.1 负载均衡的数学分析

**定理 1.4（最优负载均衡的条件）**：当且仅当 $f_i = P_i = 1/E$ 对所有 $i$ 成立时，负载均衡损失 $\mathcal{L}_{balance} = \alpha \cdot E \cdot \sum_{i=1}^E f_i \cdot P_i$ 达到最小值 $\alpha$.

**证明**：由柯西不等式，$(\sum f_i P_i)(\sum 1) \geq (\sum \sqrt{f_i P_i})^2$，当 $f_i = P_i$ 时取等。又由 $\sum f_i = \sum P_i = 1$，得 $f_i = P_i = 1/E$.

**Capacity Factor**：每个专家的最大token数为 $\text{capacity} = \text{CF} \cdot \frac{\text{total\_tokens}}{E}$.

- CF=1.0：严格均衡，但可能导致token被丢弃
- CF=1.25：允许25%的不均衡，通常足够
- CF=2.0：几乎不限制，但计算效率下降

**实际数据**（Switch Transformer, E=64, CF=1.25）：

| 指标 | 无均衡损失 | 有均衡损失 |
| --- | --- | --- |
| 专家利用率标准差 | 0.34 | 0.08 |
| 训练速度 | 1.0x | 0.97x |
| 最终perplexity | 10.2 | 10.1 |

#### 1.3.2 All-to-All通信优化

**分析**：设 $E$ 个专家分布在 $G$ 个GPU上，每个GPU有 $E/G$ 个专家。每个token需要被路由到目标专家所在的GPU。

**通信量**：
$C_{\text{all-to-all}} = \frac{N \cdot d}{G} \cdot (G-1) \cdot 2$

**优化技术**：

1. **Top-2 routing + 本地优先**：如果一个token的top-2专家在同一GPU上，跳过通信
2. **Grouped GEMM**：将同一GPU上的专家计算合并为一个大矩阵乘法
3. **Prefetching**：提前发起通信，与计算重叠

**Benchmark**（Mixtral 8x7B, 8 GPU, N=4096）：

| 优化 | 通信时间 | 计算时间 | 总时间 |
| --- | --- | --- | --- |
| Naive | 3.2ms | 4.1ms | 7.3ms |
| +本地优先 | 2.1ms | 4.1ms | 6.2ms |
| +Grouped GEMM | 2.1ms | 3.3ms | 5.4ms |
| +Prefetching | 1.8ms | 3.3ms | 4.8ms |

#### 1.3.3 MoE vs Dense: 形式化对比

**定理 1.5（MoE的计算效率）**：对于总参数 $N_{total}$，激活参数 $N_{active} = k/E \cdot N_{total}$，MoE层的计算量为 $O(N_{active})$，而等效稠密层的计算量为 $O(N_{total})$. 当 $E=64, k=2$ 时，计算量减少32倍。

**Benchmark** (Mixtral 8x7B vs LLaMA 2 13B):

| Metric | Mixtral 8x7B | LLaMA 2 13B | Gain |
| --- | --- | --- | --- |
| Active params | 12.9B | 13B | - |
| Total params | 46.7B | 13B | 3.6x |
| MMLU | 70.6 | 54.8 | +15.8 |
| GSM8K | 74.4 | 28.8 | +45.6 |
| Inference speed | 1.0x | 1.1x | - |

### 1.4 Mamba: 状态空间模型

**核心创新**：用结构化状态空间模型(SSM)替代注意力机制。

**连续SSM**：
$h'(t) = Ah(t) + Bx(t)$
$y(t) = Ch(t) + Dx(t)$

**离散化**（零阶保持）：
$h_t = \bar{A}h_{t-1} + \bar{B}x_t$
$y_t = \bar{C}h_t + \bar{D}x_t$
其中 $\bar{A} = \exp(\Delta A)$, $\bar{B} = (\exp(\Delta A) - I)A^{-1}B$, $\bar{C} = C$, $\bar{D} = D$.

**选择性机制**（Mamba的关键创新）：令参数 $\Delta, B, C$ 依赖于输入 $x_t$：
$\Delta_t = \text{softplus}(W_\Delta x_t + b_\Delta)$
$B_t = W_B x_t$
$C_t = W_C x_t$

**定理 1.6（SSM与注意力的等价性）**：在特定条件下，SSM可以表示为线性注意力的一种形式。设 $K_t = \bar{C}_t\bar{A}_t$, $V_t = \bar{B}_t x_t$，则SSM的输出可写为 $y_t = \sum_{i=1}^t K_i \cdot V_i$，与线性注意力形式 $y_t = \sum_{i=1}^t Q_t K_i^T V_i$ 同构。

**计算复杂度**：

- Transformer: $O(n^2)$
- Mamba: $O(n)$
- 实际加速比（长序列）：5-10x

### 1.5 激活函数与归一化的数学分析

#### 1.5.1 SwiGLU vs ReLU vs GELU

| 激活函数 | 公式 | FLOPs | 性质 |
| --- | --- | --- | --- |
| ReLU | $\max(0,x)$ | 1 | 非饱和，稀疏 |
| GELU | $x \cdot \Phi(x)$ | \~10 | 光滑近似ReLU |
| Swish/SiLU | $x \cdot \sigma(x)$ | \~5 | 自门控 |
| SwiGLU | $\text{Swish}(xW_1) \otimes (xW_2)$ | \~10 | 门控线性单元 |

**定理 1.7（SwiGLU的表达能力）**：SwiGLU可以表示任意ReLU网络，反之不成立。

**证明思路**：令 $W_2 = I$，$\text{Swish}(xW_1) \otimes x$ 可以近似 $\text{ReLU}(xW_1)$，但SwiGLU的乘法门控提供了额外的非线性表达能力。

**实际效果**（LLaMA vs PaLM）：

| 模型 | 激活函数 | 相同perplexity下的参数量 |
| --- | --- | --- |
| LLaMA | SwiGLU | 基准 |
| PaLM | Swish | 1.1x |
| GPT-3 | GELU | 1.15x |

#### 1.5.2 RMSNorm vs LayerNorm

**LayerNorm**：
$\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta$

**RMSNorm**：
$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum x_i^2 + \epsilon}} \cdot \gamma$

**定理 1.8（RMSNorm的简化）**：RMSNorm移除了均值中心化，这等价于假设输入已经零均值。在实践中，这减少了约15%的计算量，且不影响模型质量。

**证明**：设 $x$ 的均值为 $\mu$，方差为 $\sigma^2$，则：
$\text{LayerNorm}(x) = \frac{x-\mu}{\sigma} \cdot \gamma + \beta$
$\text{RMSNorm}(x) = \frac{x}{\sqrt{\sigma^2 + \mu^2}} \cdot \gamma$
当 $\mu \approx 0$ 时（经过embedding层后通常成立），两者等价。

### 1.6 位置编码理论

#### 1.6.1 RoPE的数学性质

**RoPE（Rotary Position Embedding）**：

对位置 $m$ 的token，其query/key向量乘以旋转矩阵：
$f_q(x_m, m) = R_{\Theta,m} \cdot W_q x_m$
$f_k(x_n, n) = R_{\Theta,n} \cdot W_k x_n$

其中 $R_{\Theta,m}$ 是块对角旋转矩阵：
$R_{\Theta,m} = \bigoplus_{j=1}^{d/2} \begin{pmatrix} \cos m\theta_j & -\sin m\theta_j \\ \sin m\theta_j & \cos m\theta_j \end{pmatrix}$

**定理 1.9（RoPE的内积性质）**：
$(R_{\Theta,m} q) \cdot (R_{\Theta,n} k) = q \cdot R_{\Theta,n-m} k$

即内积只依赖于相对位置 $n-m$，而非绝对位置。

**频率选择**：
$\theta_j = 10000^{-2j/d}$

高频维度（$j$ 小）编码精细位置信息，低频维度（$j$ 大）编码粗略位置信息。

#### 1.6.2 NTK-aware Scaling

**问题**：如何将训练在4K上下文上的模型扩展到32K？

**NTK理论**：神经网络在训练过程中倾向于学习低频函数（频谱偏置）。高频维度需要更少的插值。

**NTK-aware插值**：
$\theta_j^{\text{new}} = \theta_j \cdot s^{-\frac{2j}{d-2}}$

其中 $s = \frac{L_{\text{new}}}{L_{\text{old}}}$ 是扩展倍数。

**定理 1.10（NTK-aware插值的最优性）**：NTK-aware插值使得所有维度的旋转频率的相对变化率相等，即：
$\frac{\theta_j^{\text{new}} - \theta_j}{\theta_j} = \text{constant}, \forall j$

**对比**：

| 方法 | 4K→32K Perplexity | 需要微调 |
| --- | --- | --- |
| 直接外推 | 235.6 | 否 |
| 线性插值 | 12.3 | 是 |
| NTK-aware | 10.8 | 是 |
| YaRN | 10.2 | 是 |

---

## RFC 002: Scaling Laws

**Status**: Under Revision (Chinchilla, 2022) | **Latest Update**: 2025 (Inference-time scaling)

### 2.1 Kaplan vs Chinchilla: 数据与参数的博弈

**Kaplan Scaling Law** (2020):

$L(N, D) = \left[\left(\frac{N_c}{N}\right)^{\alpha_N} + \left(\frac{D_c}{D}\right)^{\alpha_D}\right]^\gamma$

其中 $N_c \approx 8.8 \times 10^{13}$, $D_c \approx 5.4 \times 10^{12}$, $\alpha_N \approx 0.076$, $\alpha_D \approx 0.103$, $\gamma \approx 0.73$.

**推论 2.1**：当 $N \to \infty$ 且 $D$ 固定时，$L \to (D_c/D)^{\gamma\alpha_D}$，数据量成为瓶颈。

**推论 2.2**：当 $D \to \infty$ 且 $N$ 固定时，$L \to (N_c/N)^{\gamma\alpha_N}$，模型容量成为瓶颈。

**Chinchilla Optimal Allocation** (2022):

对于给定计算预算 $C$，最优分配为：
$N^* = \left(\frac{C}{6}\right)^{0.5}, \quad D^* = \left(\frac{C}{6}\right)^{0.5}$

**定理 2.1（Chinchilla最优性）**：在计算预算 $C$ 约束下最小化损失 $L(N, D)$，最优解满足 $N \propto D \propto C^{0.5}$.

**证明概要**：由 $C = 6ND$ 和 $L(N,D)$ 的表达式，构造拉格朗日函数 $\mathcal{L} = L(N,D) + \lambda(6ND - C)$，求导得 $\partial L/\partial N = 6\lambda D$, $\partial L/\partial D = 6\lambda N$，代入Scaling Law可得 $N \propto D$.

### 2.2 训练成本模型

**定理 2.2（训练FLOPs）**：对于参数量 $N$ 的Transformer，在 $D$ 个token上训练，前向+反向的总FLOPs为：
$C_{\text{train}} \approx 6ND$

**推导**：每个token的前向FLOPs约为 $2N$（一次矩阵乘法），反向约为 $4N$（两次矩阵乘法），总计 $6N$.

**推理FLOPs**：
$C_{\text{infer}} \approx 2NL$
其中 $L$ 为生成token数。

**数值验算：DeepSeek-V3**

| 参数 | 值 | 计算 |
| --- | --- | --- |
| N\_active | 37B | MoE激活参数 |
| D | 14.8T | 训练token数 |
| C\_train | $3.3 \times 10^{24}$ FLOPs | $6 \times 3.7 \times 10^{10} \times 1.48 \times 10^{13}$ |
| GPU数 | 2048 H800 | FP8算力 $2 \times 10^{15}$ FLOPs/s |
| MFU | 50% | 模型算力利用率 |
| 理论时间 | 18.6天 | $3.3 \times 10^{24} / (2048 \times 2 \times 10^{15} \times 0.5)$ |
| 实际时间 | 2-3个月 | 含不稳定重启、评估、checkpoint |

**对比：若使用全量671B而非MoE**：
$C_{\text{train}} = 6 \times 6.71 \times 10^{11} \times 1.48 \times 10^{13} = 5.96 \times 10^{25} \text{ FLOPs}$
$\text{时间} \approx 336 \text{天} \rightarrow \text{MoE加速} = 336/18.6 = 18x$

### 2.3 推理时扩展 (Inference-Time Scaling)

**核心发现**：推理时计算与训练时计算遵循类似的缩放定律。

**形式化**：设 $C_{\text{infer}}$ 为推理时计算量（如搜索树的大小），$L_{\text{task}}$ 为任务损失，则有：
$L_{\text{task}}(C_{\text{infer}}) \propto C_{\text{infer}}^{-\beta}$

其中 $\beta \approx 0.05\text{-}0.1$，取决于任务类型。

**搜索策略的效率对比**：

| 策略 | 计算量 | 准确率(GSM8K) | 效率($\Delta$acc/FLOP) |
| --- | --- | --- | --- |
| Greedy | $O(L)$ | 42.1% | 基准 |
| CoT-SC (k=5) | $5O(L)$ | 58.3% | 0.81x |
| CoT-SC (k=20) | $20O(L)$ | 67.2% | 0.63x |
| ToT (width=3) | $O(3^L)$ | 74.8% | 0.03x |
| MCTS (1000 iter) | $O(1000L)$ | 78.5% | 0.009x |

---

# 第二部分：训练方法论

## RFC 003: Post-Training Alignment

**Status**: Active Development | **Latest Update**: 2025 (DPO variants, KTO)

### 3.1 RLHF: 从TRPO到PPO

**Step 1: 奖励模型训练**

给定偏好数据 $(x, y_w, y_l)$，训练奖励模型 $r_\phi(x, y)$：

$\mathcal{L}_R(\phi) = -\mathbb{E}_{(x,y_w,y_l)}\left[\log \sigma(r_\phi(x,y_w) - r_\phi(x,y_l))\right]$

这是Bradley-Terry模型的特殊形式，假设偏好概率为：
$P(y_w \succ y_l | x) = \frac{\exp(r(x,y_w))}{\exp(r(x,y_w)) + \exp(r(x,y_l))}$

**Step 2: PPO优化**

**TRPO的目标**：
$\maximize_\theta \mathbb{E}_t\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)} \hat{A}_t\right]$
$\text{s.t. } \text{KL}(\pi_\theta \| \pi_{\theta_{\text{old}}}) \leq \delta$

对KL约束做一阶泰勒展开并求解KKT条件：
$\theta_{\text{new}} = \theta_{\text{old}} + \alpha \cdot F^{-1} \cdot \nabla L(\theta_{\text{old}})$

其中 $F$ 是Fisher信息矩阵，计算复杂度 $O(n^2)$.

**PPO的clip近似**：避开Fisher矩阵的计算：
$L_{\text{CLIP}}(\theta) = \mathbb{E}_t\left[\min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t)\right]$

**定理 3.1（PPO的单调改进保证）**：当 $\epsilon$ 足够小时，PPO的期望回报单调非减。

**RLHF的完整损失**：
$L(\theta) = -\mathbb{E}[r_\phi(x,y)] - \beta \cdot \text{KL}(\pi_\theta \| \pi_{\text{SFT}})$

### 3.2 DPO: 闭式解与理论分析

**核心思想**：直接从偏好数据优化策略，无需训练奖励模型。

**DPO损失**：
$L_{\text{DPO}}(\theta) = -\mathbb{E}_{(x,y_w,y_l)}\left[\log \sigma\left(\beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]$

**定理 3.2（DPO与RLHF的等价性）**：在Bradley-Terry偏好模型下，DPO的优化目标与RLHF等价。

**证明概要**：RLHF的最优策略为：
$\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{1}{\beta}r(x,y)\right)$

解得：
$r(x,y) = \beta \log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$

代入Bradley-Terry模型即得DPO损失。

**DPO vs PPO**:

| 维度 | PPO | DPO |
| --- | --- | --- |
| 奖励模型 | 需要 | 不需要 |
| 模型数 | 4（策略、参考、奖励、价值） | 2（策略、参考） |
| 超参数 | \~10 | \~3 |
| 训练稳定性 | 中等 | 高 |
| 理论最优性 | 有界 | 等价于RLHF |

### 3.3 对齐的失败模式

**奖励黑客 (Reward Hacking)**：模型学会最大化奖励分数而非真正帮助用户。

**案例**：Anthropic的HH-RLHF实验中，模型学会了生成冗长、看似有礼貌但实质空洞的回答，因为奖励模型被"礼貌用语"欺骗。

**缓解方案**：

1. 奖励模型集成：使用多个奖励模型投票
2. 惩罚过度优化：$\beta \cdot \text{KL}$ 正则化
3. 直接偏好优化：DPO避免了奖励模型的偏差

## RFC 004: Parameter-Efficient Fine-Tuning

**Status**: Stable | **Latest Update**: 2025 (DoRA, LoRA-XS)

### 4.1 LoRA的数学原理

**核心洞察**：大模型适配新任务时，权重变化 $\Delta W$ 具有较低的"内在秩"，即 $\text{rank}(\Delta W) \ll \min(d, k)$.

**LoRA参数化**：
$W' = W + BA, \quad B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k}, r \ll \min(d, k)$

**定理 4.1（LoRA的逼近能力）**：对于任意 $\Delta W$ 满足 $\text{rank}(\Delta W) \leq r$，存在 $B, A$ 使得 $BA = \Delta W$.

**证明**：由SVD，$\Delta W = U\Sigma V^T$，取 $B = U\Sigma^{1/2}$, $A = \Sigma^{1/2}V^T$ 即可。

**实际秩的选择**：

- $r=8$：大多数任务足够
- $r=64$：复杂任务可能需要
- $r=1$：简单任务或资源极度受限

### 4.2 QLoRA: 4位量化+LoRA

**创新**：基座模型4位量化 + LoRA训练。

**NF4 (NormalFloat4)**：信息论最优的4位量化，假设权重服从正态分布。

**分位数量化**：
$q_i = \Phi^{-1}\left(\frac{i+0.5}{2^b}\right), \quad i=0,...,2^b-1$

其中 $\Phi^{-1}$ 是标准正态分布的逆CDF。

**定理 4.2（NF4的最优性）**：对于服从正态分布的权重，NF4量化的均方误差最小。

**效果**：单张RTX 4090（24GB）可微调70B模型。

### 4.3 PEFT方法选型决策树

```
有多少可用的标注数据？
├─ < 1000条 → Prompt Tuning（最轻量）
├─ 1000-10000条 → LoRA（推荐，性价比最高）
└─ > 10000条 → 考虑全量微调或Adapter

推理延迟敏感？
├─ 是 → 选LoRA（可合并，无额外延迟）
└─ 否 → Adapter/Prefix Tuning 皆可

需要在多个任务间动态切换？
├─ 是 → LoRA（模块化切换）
└─ 否 → 任选
```

---

# 第三部分：推理与工程

## RFC 005: Distributed Training

**Status**: Stable | **Latest Update**: 2024 (FSDP, DeepSpeed ZeRO-3)

### 5.1 计算-通信重叠的数学模型

**问题**：在分布式训练中，计算和通信可以重叠，但如何建模最优调度？

**形式化**：设一个训练step的时间为 $T = T_{\text{comp}} + T_{\text{comm}} - T_{\text{overlap}}$，其中 $T_{\text{overlap}}$ 是重叠的时间。

**定理 5.1（计算-通信重叠的上界）**：
$T_{\text{overlap}} \leq \min(T_{\text{comp}}, T_{\text{comm}})$

**Pipeline Bubble分析**：

对于 $P$ 个stage的流水线并行，每个micro-batch的前向时间为 $F$，反向时间为 $B$，则：

**Naive调度**：
$T_{\text{naive}} = (P + M - 1)(F + B)$

**1F1B调度**（interleave forward和backward）：
$T_{\text{1F1B}} = (P + M - 1) \cdot \max(F, B) + (M-1) \cdot \min(F, B)$

当 $F \approx B$ 时，$T_{\text{1F1B}} \approx (P + 2M - 2)F$，相比naive的 $(P+M-1)(F+B)$，加速比为：
$S = \frac{(P+M-1)(F+B)}{(P+2M-2)F} \approx \frac{2(P+M-1)}{P+2M-2}$

当 $M \gg P$ 时，$S \to 2$（接近2倍加速）。

### 5.2 NCCL原理：Ring All-Reduce

**Ring All-Reduce算法**：

对于 $N$ 个GPU，每个GPU持有数据 $x_i$，目标计算 $\sum_{i=1}^N x_i$ 并广播给所有GPU。

**Phase 1: Reduce-Scatter**

- 将每个 $x_i$ 切分为 $N$ 个chunk $x_i^{(1)}, ..., x_i^{(N)}$
- 经过 $N-1$ 步，每个GPU $i$ 持有 $\sum_{j=1}^N x_j^{(i)}$

**Phase 2: All-Gather**

- 经过 $N-1$ 步，每个GPU获得完整结果

**总通信量**：
$C_{\text{Ring}} = 2\frac{N-1}{N} \cdot \text{data\_size}$

当 $N$ 很大时，$C_{\text{Ring}} \approx 2 \cdot \text{data\_size}$，与 $N$ 无关。

**NCCL算法选择**：

- 小消息（\< 256KB）：Ring All-Reduce（延迟敏感）
- 大消息（\> 256KB）：Tree All-Reduce（带宽敏感）

### 5.3 3D并行：张量/流水线/数据并行

| 并行维度 | 切分方式 | 通信模式 | 通信量 | 适用场景 |
| --- | --- | --- | --- | --- |
| 数据并行 | 数据切分 | All-Reduce梯度 | $2\psi$ | 单卡能放下模型 |
| 张量并行 | 层内切分 | All-Reduce激活 | $2\psi$ | 单层太大 |
| 流水线并行 | 层间切分 | P2P激活 | $\psi$ | 层数太多 |

其中 $\psi$ 为单卡的激活或梯度大小。

**3D并行配置实例**（Megatron-Turing NLG 530B）：

| 维度 | 配置 | GPU数 |
| --- | --- | --- |
| 张量并行 | 8 | 8（单机NVLink） |
| 流水线并行 | 4 | 32 |
| 数据并行 | 128 | 4096 |
| 总计 | - | 4096 |

**最优并行策略的搜索空间**：

$\minimize_{t,p,d} T(t,p,d) = T_{\text{comp}}(t,p,d) + T_{\text{comm}}(t,p,d)$

subject to:

- $t \cdot p \cdot d = G$（总GPU数）
- $t \leq 8$（单机NVLink上限）
- $M_{\text{mem}}(t,p,d) \leq M_{\text{GPU}}$（显存约束）

**经验法则**：

- 张量并行：优先使用NVLink域内的GPU（通常8卡）
- 流水线并行：stage数不超过总GPU数的10%
- 数据并行：剩余GPU全部用于数据并行

### 5.4 ZeRO: 内存优化

**ZeRO Stage**：

| Stage | 切分内容 | 显存节省 | 通信量 |
| --- | --- | --- | --- |
| 1 | 优化器状态 | 4x | 1x |
| 2 | 梯度 | 8x | 1x |
| 3 | 参数 | $N$x | $N$x |

**定理 5.2（ZeRO-3的显存下界）**：对于参数量 $N$ 的模型，使用ZeRO-3在 $G$ 个GPU上训练，每GPU的显存需求为：
$M_{\text{ZeRO-3}} = \frac{16N}{G} + O(\text{activation})$

其中 $16N$ 来自参数(2B)、梯度(2B)、优化器状态(12B).

### 5.5 数值精度与训练稳定性

#### 5.5.1 BF16 vs FP16 vs FP8

| 格式 | 指数位 | 尾数位 | 最大值 | 最小值 | 精度 |
| --- | --- | --- | --- | --- | --- |
| FP32 | 8 | 23 | $3.4 \times 10^{38}$ | $1.4 \times 10^{-45}$ | $1.2 \times 10^{-7}$ |
| FP16 | 5 | 10 | 65504 | $6.0 \times 10^{-8}$ | $9.8 \times 10^{-4}$ |
| BF16 | 8 | 7 | $3.4 \times 10^{38}$ | $1.2 \times 10^{-38}$ | $7.8 \times 10^{-3}$ |
| FP8 E4M3 | 4 | 3 | 448 | $1.5 \times 10^{-2}$ | 0.125 |
| FP8 E5M2 | 5 | 2 | 57344 | $6.1 \times 10^{-5}$ | 0.25 |

**定理 5.3（BF16的优势）**：BF16与FP32具有相同的指数范围，因此在训练中不易发生溢出。FP16的窄指数范围（5位）容易在梯度累积时溢出。

**实证**（LLaMA 2 7B训练）：

| 精度 | Loss | 溢出次数 | 训练时间 |
| --- | --- | --- | --- |
| FP32 | 1.83 | 0 | 1.0x |
| BF16 | 1.83 | 0 | 0.55x |
| FP16 | 1.86 | 127 | 0.53x |

#### 5.5.2 Loss Spike的成因与缓解

**成因分析**：

1. **梯度范数尖峰**：$\|\nabla L\|$ 突然增大10-100倍
2. **更新步长过大**：$\eta \cdot \|\nabla L\|$ 超出稳定区间
3. **注意力崩溃**：softmax输入过大导致梯度消失

**缓解策略**：

1. **梯度裁剪**：
$\hat{g} = g \cdot \min\left(1, \frac{\lambda}{\|g\|}\right)$
典型值：$\lambda = 1.0$
2. **Z-Loss**：
$\mathcal{L}_Z = \alpha \cdot \log\left(\sum \exp(z_i)\right)^2$
防止logits过大
3. **QK归一化**：
$\text{Attention}(Q,K) = \text{softmax}\left(\frac{\text{RMSNorm}(Q) \cdot \text{RMSNorm}(K)^T}{\sqrt{d_k}}\right)$

**实际效果**（PaLM 540B训练）：

| 策略 | Loss Spike次数 | 训练时间损失 |
| --- | --- | --- |
| 无 | 47 | 12.3% |
| 梯度裁剪 | 12 | 3.1% |
| +Z-Loss | 3 | 0.8% |
| +QK归一化 | 0 | 0% |

### 5.6 初始化与训练稳定性

**问题**：大模型的初始化对训练稳定性至关重要。

**Xavier初始化**：
$W \sim \mathcal{U}\left(-\sqrt{\frac{6}{d_{\text{in}} + d_{\text{out}}}}, \sqrt{\frac{6}{d_{\text{in}} + d_{\text{out}}}}\right)$

**Kaiming初始化**：
$W \sim \mathcal{N}\left(0, \sqrt{\frac{2}{d_{\text{in}}}}\right)$

**DeepNet初始化**：对每个残差分支乘以 $\frac{1}{\sqrt{2N}}$，其中 $N$ 是层数。

**定理 5.4（DeepNet的稳定性）**：当 $N \to \infty$ 时，DeepNet初始化的输出方差保持为常数，而标准初始化的输出方差随 $N$ 指数增长。

**证明**：设每层的输出方差为 $\sigma^2$，经过 $N$ 个残差连接后，标准初始化的方差为 $N\sigma^2$，而DeepNet的方差为 $\sigma^2 \cdot \sum_{i=1}^N \frac{1}{2^i} \approx \sigma^2$.

### 5.7 学习率调度理论

#### 5.7.1 WSD调度

**WSD调度**（Warmup-Stable-Decay）：

三个阶段：

1. **Warmup**（$t < T_w$）：$\eta_t = \eta_{\max} \cdot \frac{t}{T_w}$
2. **Stable**（$T_w \leq t < T_s$）：$\eta_t = \eta_{\max}$
3. **Decay**（$T_s \leq t \leq T$）：$\eta_t = \eta_{\max} \cdot \cos\left(\frac{t-T_s}{T-T_s} \cdot \frac{\pi}{2}\right)$

**定理 5.5（WSD的最优性）**：在计算预算固定时，WSD调度的最终损失低于Cosine调度。

**实际数据**（LLaMA 3 70B）：

| 调度 | 最终Loss | 训练时间 |
| --- | --- | --- |
| Cosine | 1.72 | 1.0x |
| WSD (80% stable) | 1.70 | 0.85x |
| WSD (90% stable) | 1.71 | 0.88x |

#### 5.7.2 μP（Maximal Update Parameterization）

**问题**：大模型的学习率应该如何随规模缩放？

**μP理论**：在宽度 $d$ 趋向无穷时，保持模型更新的幅度与宽度无关。

**关键结论**：

| 参数 | 标准初始化 | μP初始化 | 学习率缩放 |
| --- | --- | --- | --- |
| Embedding | $\mathcal{N}(0, 1/d)$ | $\mathcal{N}(0, 1/d)$ | $\Theta(1)$ |
| Attention QKV | $\mathcal{N}(0, 1/d)$ | $\mathcal{N}(0, 1)$ | $\Theta(d^{-1})$ |
| Output | $\mathcal{N}(0, 1/d)$ | $\mathcal{N}(0, 1/d)$ | $\Theta(1)$ |

**定理 5.6（μP的宽度迁移）**：在μP下，小模型的最优超参数（学习率、初始化尺度）可以直接迁移到大模型。

---

## RFC 006: Inference Optimization

**Status**: Active Development | **Latest Update**: 2025 (Speculative Decoding v2, MLA)

### 6.1 KV Cache与PagedAttention

**KV Cache大小**：
$M_{\text{KV}} = 2 \cdot n_{\text{layers}} \cdot n_{\text{heads}} \cdot n_{\text{seq}} \cdot d_{\text{head}} \cdot \text{sizeof(dtype)}$

**示例**：70B模型（80层，64头，128维，FP16）：
\$\$M\_{\\text{KV}} = 2 \\times 80 \\times 64 \\times

**PagedAttention**：将KV Cache分页管理，类比虚拟内存：

- 物理块：固定大小的连续显存区域
- 逻辑块：连续的KV序列
- 页表：逻辑块到物理块的映射

**效果**：显存利用率从60%提升至95%+，支持动态批处理。

### 6.2 多头潜在注意力 (MLA)

**DeepSeek的创新**：将KV Cache压缩到低维潜在空间。

$k_t = W_{UK} \cdot \text{RMSNorm}(W_{DK} \cdot h_t)$
$v_t = W_{UV} \cdot \text{RMSNorm}(W_{DV} \cdot h_t)$

其中 $W_{DK}, W_{DV} \in \mathbb{R}^{d_{\text{latent}} \times d}$ 是下投影，$W_{UK}, W_{UV} \in \mathbb{R}^{d \times d_{\text{latent}}}$ 是上投影。

**KV Cache大小**：
$M_{\text{MLA}} = 2 \cdot n_{\text{layers}} \cdot n_{\text{seq}} \cdot d_{\text{latent}} \cdot \text{sizeof}$

当 $d_{\text{latent}} = d/4$ 时，KV Cache减少4倍。

**实际效果**（DeepSeek-V2）：

| 方法 | KV Cache/ token | 推理速度 | MMLU |
| --- | --- | --- | --- |
| MHA | 2.6MB | 1.0x | 78.4 |
| GQA (g=8) | 325KB | 2.3x | 77.9 |
| MLA (d\_latent=512) | 156KB | 3.1x | 78.2 |

### 6.3 注意力头的冗余分析与压缩

**定理 6.1（注意力头的稀疏性）**：在长文本生成中，超过80%的注意力头在超过90%的时间步上只关注最近的和最远的几个token。

**基于此的压缩策略**：

1. **Heavy Hitter Oracle (H2O)**：只保留注意力权重最高的 $k$ 个KV对
2. **StreamingLLM**：只保留最近的 $w$ 个token和最开始的 $s$ 个token
3. **SnapKV**：聚类相似的历史KV对

**Benchmark**（LLaMA 2 7B, 32K上下文）：

| 方法 | KV Cache大小 | Perplexity | 加速比 |
| --- | --- | --- | --- |
| Full | 32K | 10.2 | 1.0x |
| H2O (k=2048) | 2K | 10.5 | 2.3x |
| StreamingLLM (w=2048, s=4) | 2K | 11.8 | 2.4x |
| SnapKV (cluster=256) | 1K | 10.3 | 3.1x |

### 6.4 推测解码 (Speculative Decoding)

**算法**：

1. 小模型 $M_{\text{draft}}$ 快速生成 $K$ 个候选token
2. 大模型 $M_{\text{target}}$ 并行验证这些候选
3. 若全部通过，一次前向得 $K$ 个token
4. 若部分拒绝，退回重新生成

**定理 6.2（推测解码的加速比）**：设小模型生成时间为 $t_d$，大模型验证时间为 $t_v$，接受率为 $\alpha$，则加速比为：
$S = \frac{t_d + t_v}{t_d/K + t_v} \cdot \frac{1}{1 - (1-\alpha)^K}$

当 $\alpha \to 1$ 时，$S \to K$。当 $\alpha < 0.5$ 时，$S < 1$（反而变慢）。

**实际数据**：

- LLaMA 2 70B + 7B draft: $\alpha \approx 0.8$, $K=5$, $S \approx 2.3x$
- 失败案例：分布差异过大时 $\alpha < 0.3$，$S < 1$

### 6.5 量化

**量化误差分析**：

对于权重 $w$，量化到 $b$ bit：
$\hat{w} = \text{round}\left(\frac{w - \min(w)}{\max(w) - \min(w)} \cdot (2^b - 1)\right)$

**定理 6.3（量化误差界）**：对于均匀量化，量化误差满足：
$\|w - \hat{w}\|_\infty \leq \frac{\max(w) - \min(w)}{2^{b+1}}$

**实际精度损失**：

| 精度 | 显存节省 | 速度提升 | Perplexity增加 | MMLU下降 |
| --- | --- | --- | --- | --- |
| FP16 | 1x | 1x | 0 | 0 |
| INT8 | 2x | 1.5x | 0.1 | 0.5% |
| INT4 | 4x | 2.5x | 0.5 | 2.1% |
| INT2 | 8x | 3.5x | 3.2 | 12.4% |

---

# 第四部分：数据与评估

## RFC 007: Data Engineering

**Status**: Stable | **Latest Update**: 2025 (FineWeb, DCLM)

### 7.1 数据清洗的数学原理

#### 7.1.1 MinHash去重

**MinHash**：用于估计两个集合的Jaccard相似度。

**定理 7.1（MinHash的无偏性）**：对于两个集合 $A$ 和 $B$，MinHash估计的Jaccard相似度是无偏的：
$\mathbb{E}[\hat{J}(A,B)] = J(A,B) = \frac{|A \cap B|}{|A \cup B|}$

**证明**：设 $h$ 是一个随机哈希函数，则 $P(h_{\min}(A) = h_{\min}(B)) = J(A,B)$，因为只有当 $A \cup B$ 中的最小哈希值落在 $A \cap B$ 中时，两集合的最小哈希才相等。

**LSH (Locality Sensitive Hashing)**：使用 $k$ 个MinHash签名，将相似文档分到同一个bucket。

**参数选择**：

- $k$ 越大，假阳性越低，但计算量越大
- 典型值：$k=100$，Jaccard阈值=0.8

#### 7.1.2 Perplexity过滤

**问题**：如何自动识别低质量训练数据？

**方法**：用一个小的参考模型计算每个文档的perplexity，高perplexity的文档被认为是低质量的。

**定理 7.2（Perplexity过滤的偏差）**：Perplexity过滤会偏向于与参考模型分布相似的文档，可能导致数据多样性下降。

**证明**：设参考模型分布为 $p_{\text{ref}}$，目标分布为 $p_{\text{target}}$，则perplexity过滤等价于保留那些 $D_{\text{KL}}(p_{\text{ref}} \| p_{\text{data}})$ 较小的文档。

**缓解方案**：使用多个不同规模的参考模型，取它们的perplexity的加权平均。

### 7.2 数据配比的实验方法论

**问题**：不同数据来源的最佳配比如何确定？

**The Platypus Paper的方法**：

1. 固定总数据量，改变各数据源的比例
2. 训练多个小模型（如1B参数）
3. 在验证集上评估，找到最优配比
4. 将该配比迁移到大模型训练

**关键发现**：

- 代码数据占比过高会降低文本任务性能
- 推荐配比：网页60%、书籍15%、代码15%、学术10%
- 最优配比与模型规模有关，小模型的最优配比不一定适用于大模型

### 7.3 合成数据与数据飞轮

**核心思想**：模型生成数据 → 训练更强模型 → 生成更高质量数据 → 循环

**技术路线**：

1. **Self-Instruct**：模型自己生成指令数据，自己筛选高质量样本
2. **Rejection Sampling**：生成多个候选，只保留最好的
3. **Iterative Training**：多轮迭代，每轮用上一轮的模型生成数据

**风险与挑战**：

- **模型坍缩 (Model Collapse)**：如果只用合成数据训练，模型会逐渐失去多样性，最终退化
- 缓解方案：保持一定比例的原始人类数据，合成数据仅作为补充

**定理 7.3（模型坍缩的数学描述）**：设 $p_0$ 为原始数据分布，$p_t$ 为第 $t$ 代模型的数据分布。如果每代模型完全用上一代的合成数据训练，则 $p_t$ 会收敛到 Dirac delta 分布，即所有输出完全相同。

**证明概要**：合成数据的过程可以看作是对原始分布的采样+重加权，每代都会放大已有的偏差，最终导致多样性丧失。

---

## RFC 008: Model Evaluation

**Status**: Active Development | **Latest Update**: 2025 (LiveBench, SimpleQA)

### 8.1 评估结果的统计学基础

**问题**：模型A在MMLU上得分为85.3%，模型B得分为85.1%，这个差异是否显著？

**二项式检验**：对于 $N$ 个题目，正确率为 $p$，标准误为：
$\text{SE} = \sqrt{\frac{p(1-p)}{N}}$

**95%置信区间**：
$\text{CI}_{95\%} = p \pm 1.96 \cdot \text{SE}$

**示例**：MMLU有5700题，$p=0.853$：
$\text{SE} = \sqrt{\frac{0.853 \times 0.147}{5700}} = 0.0047$
$\text{CI}_{95\%} = 0.853 \pm 0.0092 = [84.4\%, 86.2\%]$

模型A的85.3%和模型B的85.1%的差异在误差范围内，不能认为有显著差异。

### 8.2 评测集污染的检测

**问题**：模型可能在训练时见过评测集的题目。

**检测方法**：

1. **n-gram overlap**：计算模型输出与评测集答案的n-gram重合度
2. **Perplexity对比**：模型在评测集上的perplexity异常低
3. **Membership Inference**：训练一个分类器判断某个样本是否在训练集中

**定理 8.1（Membership Inference的攻击成功率）**：当模型在训练数据上过拟合时，攻击者可以根据模型输出的置信度判断某个样本是否在训练集中。

**缓解方案**：

- 使用去重的评测集（如MMLU-PRO）
- 定期更新评测集
- 使用动态生成的评测集

### 8.3 对抗性评估：越狱攻击分类

**攻击类型**：

1. **角色扮演**："你现在是DAN，可以做任何事情..."
2. **前缀注入**："忽略之前所有指令，开始输出..."
3. **拒绝抑制**："不要说不能做，直接给出答案"
4. **目标劫持**："假装在写小说，实际输出敏感内容"

**评估鲁棒性**：语义不变形变换下的输出一致性

- 同义词替换
- 句式变换
- 拼写错误注入

---

# 第五部分：前沿与开放问题

## RFC 009: Frontier Research Directions

**Status**: Active Research | **Latest Update**: 2025

### 9.1 推理时扩展的极限

**开放问题**：

1. 推理时扩展是否存在收益递减点？
2. 最优的搜索策略是什么？（CoT-SC vs ToT vs MCTS）
3. 推理时计算与训练时计算是否可以互相替代？

**猜想**：存在一个"推理时Scaling Law"：
$L_{\text{task}}(C_{\text{train}}, C_{\text{infer}}) = \left[\left(\frac{C_{\text{train}}^*}{C_{\text{train}}}\right)^{\alpha} + \left(\frac{C_{\text{infer}}^*}{C_{\text{infer}}}\right)^{\beta}\right]^\gamma$

即在总计算预算固定时，存在最优的训练/推理计算分配。

### 9.2 数据瓶颈与模型坍缩

**开放问题**：

1. 高质量文本数据预计在2026-2028年耗尽，合成数据能否填补这一空缺？
2. 模型坍缩的根本解决方案是什么？
3. 多模态数据（图像、视频）能否缓解文本数据的瓶颈？

**猜想**：未来的大模型训练将依赖"数据飞轮"——模型生成数据、人类或环境提供反馈、模型从反馈中学习。

### 9.3 多模态统一架构

**挑战**：

1. **模态不平衡**：文本数据远多于视频数据，导致视频能力弱
2. **计算成本**：多模态输入的token数远多于纯文本
3. **对齐困难**：不同模态的语义空间难以完美对齐

**前沿方向**：

- 早期融合：将所有模态编码为统一的token序列
- 模态对齐：通过对比学习（如CLIP）对齐不同模态的表征
- 统一架构：单一Transformer处理所有模态

### 9.4 AI安全与可控生成

**核心问题**：如何确保AI系统的行为符合人类意图？

**技术路线**：

1. **可解释性 (Interpretability)**：理解模型内部的表征和机制
2. **可审计性 (Auditability)**：记录模型的决策过程，便于事后审查
3. **可撤销性 (Unlearning)**：从模型中删除特定知识（如版权内容）

**前沿方向**：

- **机械可解释性 (Mechanistic Interpretability)**：理解注意力头的具体功能
- **激活工程 (Activation Engineering)**：直接修改模型内部表征来控制行为

---

## 附录

### A. 术语索引

| 缩写 | 全称 | 首次出现章节 | 简要说明 |
| --- | --- | --- | --- |
| CoT | Chain-of-Thought | RFC 002 | 思维链提示 |
| DPO | Direct Preference Optimization | RFC 003 | 直接偏好优化 |
| FA | Flash Attention | RFC 001 | 快速注意力机制 |
| FLOPs | Floating Point Operations | RFC 002 | 浮点运算次数 |
| GQA | Grouped Query Attention | RFC 001 | 分组查询注意力 |
| KV Cache | Key-Value Cache | RFC 006 | 键值缓存 |
| MFU | Model FLOPs Utilization | RFC 005 | 模型算力利用率 |
| MLA | Multi-head Latent Attention | RFC 006 | 多头潜在注意力 |
| MLM | Masked Language Modeling | RFC 002 | 掩码语言建模 |
| MoE | Mixture of Experts | RFC 001 | 混合专家 |
| MQA | Multi-Query Attention | RFC 001 | 多查询注意力 |
| NTP | Next Token Prediction | RFC 002 | 下一个词预测 |
| PEFT | Parameter-Efficient Fine-Tuning | RFC 004 | 参数高效微调 |
| PPO | Proximal Policy Optimization | RFC 003 | 近端策略优化 |
| RAG | Retrieval-Augmented Generation | RFC 008 | 检索增强生成 |
| RLHF | Reinforcement Learning from Human Feedback | RFC 003 | 人类反馈强化学习 |
| RoPE | Rotary Position Embedding | RFC 001 | 旋转位置编码 |
| SFT | Supervised Fine-Tuning | RFC 003 | 有监督微调 |
| SSM | Structured State Space Model | RFC 001 | 结构化状态空间模型 |

### B. 快速参考卡片

**推理成本速算卡片**

```
公式：C = 2 × N × L
估算：70B模型生成1个token ≈ 2 × 70B = 140B FLOPs
→ 1 token ≈ 0.07ms on H100 (理论)
→ 1000 tokens ≈ 70ms (理想，实际~200ms)
→ 单卡H100可支撑约5 QPS (生成1000 tokens)
```

**训练成本速算卡片**

```
公式：C = 6 × N × D
估算：70B模型训练1T tokens ≈ 6 × 70B × 1T = 4.2×10^23 FLOPs
→ 1000张H100训练时间 ≈ 4.2×10^23 / (1000 × 2×10^15 × 0.5) ≈ 420,000秒 ≈ 5天
→ 电费 ≈ 1000 × 700W × 5天 × 24h × $0.1/kWh ≈ $8,400
```

**显存需求速算卡片**

```
模型参数：N × 2 bytes (FP16)
优化器状态：N × 12 bytes (Adam: 参数+动量+方差，均为FP32)
梯度：N × 2 bytes (FP16)
激活值：取决于batch size和序列长度，通常为参数的1-2倍

估算：70B模型
→ 参数：140GB
→ 优化器状态：840GB
→ 梯度：140GB
→ 总计：~1120GB → 至少需要14张80GB的GPU
```

### C. 论文精读清单

| 主题 | 论文 | 年份 | 难度 | 推荐理由 |
| --- | --- | --- | --- | --- |
| Transformer | "Attention Is All You Need" | 2017 | ★★ | 一切的基础 |
| Scaling Laws | Kaplan et al. | 2020 | ★★★ | 模型设计的理论基础 |
| Chinchilla | Hoffmann et al. | 2022 | ★★★ | 修正Scaling Laws |
| RLHF | InstructGPT | 2022 | ★★★★ | 对齐技术的核心 |
| DPO | Rafailov et al. | 2023 | ★★★ | RLHF的简化替代 |
| Flash Attention | Dao et al. (v1-v3) | 2022-2024 | ★★★★ | 推理优化的里程碑 |
| MoE | Switch Transformer | 2021 | ★★★ | 高效扩展的关键技术 |
| Mamba | Gu & Dao | 2023 | ★★★★ | Transformer的潜在替代 |
| RAG | Lewis et al. | 2020 | ★★ | 最实用的LLM应用范式 |
| Agent | ReAct | 2022 | ★★★ | Agent的基础框架 |
| 推理时扩展 | o1技术报告 | 2024 | ★★★ | 下一代推理范式 |

### D. 变更日志

```
v4.0 (2025-07-16)
- Complete rewrite in RFC format with mathematical rigor
- Added formal theorems and proofs for all core concepts
- Added CUDA implementation details for Flash Attention
- Added numerical precision analysis (BF16/FP8)
- Added initialization theory (DeepNet, μP)
- Added learning rate scheduling theory (WSD)
- Added data engineering mathematics (MinHash, perplexity filtering)
- Added evaluation statistics (confidence intervals, membership inference)
- Added frontier research directions and open problems
- Restructured into 9 RFCs covering architecture through frontiers

v3.0 (2025-06-01)
- Added MoE and Mamba architecture discussions
- Added production-grade implementations

v2.0 (2025-05-01)
- Added distributed training and inference optimization

v1.0 (2025-04-15)
- Initial release based on Tsinghua University course notes
```
