# ⚙️ GEAR · GPU Energy-Aware Runtime

> 一套面向 GPU 的**能耗感知运行时**：动态电压频率调整（DVFS）、功耗/频率封顶、温度保护，以及"可回收废热"度量。
> 目标：**在不损失吞吐的前提下，最小化 GPU 能耗与峰值功耗。**

---

## 为什么值得做

大模型训练/推理的 GPU 账单已成数据中心最大开销之一。以 DeepSeek-V3 为例：671B MoE、约 2.79M H800 GPU·小时、约 **$5.6M** 算力成本。**能效优化直接削减这块成本**：

- 功耗封顶 / DVFS 每省 **20–30% 能耗**，在数百万美元的训练预算上就是**真正的 ROI**；
- 这不是环保口号，是成本工程。

> 训练成本快速估算见 [`scripts/estimate_cost.py`](scripts/estimate_cost.py)。

## 功能

| 模块 | 作用 |
|---|---|
| `DVFSController` | 动态调频 + 功耗/频率封顶 + ML 预测最优频率 |
| `ThermalManager` | 温度采集、热状态分级、过热降频、可回收废热度量 |
| `GPUPowerOptimizer` | 一行代码套用保守功耗优化（NVIDIA/AMD） |
| CLI 遥测仪表盘 | 实时展示温度/功耗/频率/利用率/能耗/性能功耗比 |

## 运行模式

| 模式 | 策略 |
|---|---|
| `max` | 跑满，不设限 |
| `balanced` | 75% 功耗 + 中高档频率 |
| `save` | 最低功耗 + 最低频率 |
| `optimal` | **能效最优**：ML 预测/启发式选频 |
| `thermal` | **温度感知**：接近峰值时逐级降频 |

## 快速开始（纯软件模拟，无需 GPU）

```bash
cd software
python main.py --simulate --mode optimal

# 常规模
python main.py --mode thermal --gpu 0
python main.py --mode max --power-limit 250

# 一行功耗优化
python -c "from core.power_optimizer import optimize_gpu; print(optimize_gpu())"

# 训练成本估算
python ../scripts/estimate_cost.py --params 671 --tokens 14800 --gpu H100
```

安装真实硬件依赖：`pip install -r requirements.txt`（`pynvml` 缺了会降级为模拟）。

## 评估方法论

- **基准**：LLM 推理（vLLM）/ MLPerf / HPC kernels / 训练 step。
- **指标**：`perf-per-watt`（FLOPS/W、tokens/s/W）、Energy-Delay Product、峰值功耗、p99 延迟。
- **对照**：基线（默认策略）vs 本系统 vs 仅功耗封顶 vs ML 预测。
- **结论**：**跑出真实数据后再下结论**。当前 README 不含未经验证的"降低 X%"声明。

## 目录结构

```
GPU-BBQ-System/  (GEAR)
├── software/
│   ├── main.py                    # CLI 遥测仪表盘
│   ├── core/dvfs_controller.py     # DVFS + 功耗/频率封顶 + ML 调频
│   ├── core/thermal_manager.py     # 热管理 + 可回收废热
│   ├── core/power_optimizer.py     # 一行功耗优化
│   └── configs/gear_config.yaml    # 配置
├── scripts/
│   ├── calibrate.py                # 实测拟合 P≈α·f^β
│   ├── run_benchmark.py            # 基准测试
│   └── estimate_cost.py            # 训练成本估算
├── tests/                          # pytest（无需 GPU/numpy）
├── models/                         # ML 能效模型占位
├── pyproject.toml                  # 项目元数据 / ruff / mypy / pytest
└── .github/workflows/ci.yml        # lint + test + compile
```

## 校准 & 扩展

1. **校准功率模型**：`python scripts/calibrate.py` → 用实测 (频率, 功耗) 拟合 `P ≈ α·f^β`，把 `ALPHA/BETA` 写回 `DVFSController`。
2. **训练 ML 模型**：用真实测量采集 `[utilization, sm_occupancy, power, temperature] → optimal_freq`，训练 RandomForest/XGBoost 并存到 `models/`。
3. **接入真实吞吐**：把业务吞吐（tokens/s 等）喂给 `perf-per-watt`，才能真正评估能效。

## 许可

- 软件：**MIT**（见 `LICENSE.md`）

---

> ⚠️ 说明：本仓库聚焦**软件能效管理**。涉及真实硬件的改频/封顶请在受控环境操作，并遵守厂商与数据中心规范。
