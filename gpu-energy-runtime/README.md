# ⚙️ GEAR · GPU Energy-Aware Runtime

> 一套面向 GPU 的**能耗感知运行时**：动态电压频率调整（DVFS）、功耗/频率封顶、温度保护与可回收废热度量。
> 核心目标：**在不损失吞吐（throughput）的前提下，最小化 GPU 能耗与峰值功耗。**

**状态**：活跃开发 · **语言**：Python 3.9+ · **许可**：MIT · **硬件**：NVIDIA（NVML）/ AMD（ROCm 适配中）

---

## 目录

- [为什么值得做](#为什么值得做)
- [功能总览](#功能总览)
- [系统架构](#系统架构)
- [运行模式](#运行模式)
- [安装](#安装)
- [快速开始](#快速开始)
- [CLI 参考](#cli-参考)
- [模块 API 参考](#模块-api-参考)
- [配置参考](#配置参考)
- [ML 能效预测](#ml-能效预测)
- [评估方法论](#评估方法论)
- [校准](#校准)
- [测试](#测试)
- [项目结构](#项目结构)
- [路线图](#路线图)
- [贡献](#贡献)
- [许可](#许可)
- [安全说明](#安全说明)
- [FAQ](#faq)

---

## 为什么值得做

大模型训练与推理的 GPU 账单，已经成为 AI 数据中心最重的运营成本之一。以 DeepSeek-V3 为例：671B 参数的 MoE 模型、约 2.79M 个 H800 GPU·小时、约 **$5.6M** 的算力成本。**能效优化直接削减这笔经费**：

- 通过 **功耗封顶（power capping）+ DVFS 动态调频**，在控制吞吐损失的前提下通常可降低 **20–30%** 的总能耗；
- 在数百万美元的训练预算上，这代表**实打实的成本节省**（ROI），而非纯粹的环保口号；
- 对**长时推理服务**（如在线 LLM API）而言，能耗是持续的电费与散热支出，收益随时间线性累积。

本项目把"省电"做成**可度量的工程**：提供统一的状态采集、策略决策、约束执行与报告接口，让你在实测数据上验证能效收益。

> 训练/微调成本快速估算见 [`scripts/estimate_cost.py`](scripts/estimate_cost.py)，支持按参数量、token 量、GPU 型号估算 FLOPs、GPU·小时与电费。

## 功能总览

| 模块 | 职责 | 关键能力 |
|---|---|---|
| `DVFSController` | 动态调频与功耗约束 | 功耗封顶、频率封顶、模式切换、ML 最优频率预测、温度感知降频、能效报告 |
| `ThermalManager` | 热状态与废热管理 | 温度采集、热状态分级（5 级）、冷却液流控（PID 简化）、可回收废热度量、降频建议 |
| `GPUPowerOptimizer` | 通用功耗优化 | NVIDIA / AMD 自动检测、一键保守优化、节能档、单行接口 |
| CLI 遥测仪表盘 (`main.py`) | 实况监控 | 温度/功耗/频率/利用率/累计能耗/性能功耗比、单帧预览 `--once`、模拟/真机双模式 |

**亮点**：

- **无硬件也能跑**：缺少 `pynvml` 或用 `--simulate` 时，自动降级为模拟传感器，适合教学、演示与 CI；
- **ML 驱动**：可加载 `RandomForest / XGBoost` 模型预测能效最优频率；无模型时自动退回启发式策略；
- **可测试**：策略与温控逻辑为纯函数设计，不依赖真实 GPU，`pytest` 即可覆盖。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI 遥测仪表盘  (main.py)                  │
│   实时监控 / 单帧预览 / 模式切换 / 报告                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ 调用
┌──────────────────────────▼──────────────────────────────────┐
│                    控制策略层 (core/)                        │
│   DVFSController  ── 动态调频 + 功耗封顶 + ML 预测 + 温度感知 │
│   ThermalManager  ── 热状态分级 + 冷却流控 + 可回收废热        │
│   GPUPowerOptimizer ─ 通用功耗优化（NVIDIA/AMD）              │
└──────────────────────────┬──────────────────────────────────┘
                           │ 读取 / 写入
┌──────────────────────────▼──────────────────────────────────┐
│                    硬件控制 API 层                            │
│   NVML / nvidia-smi   ·   ROCm (rocm-smi)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    硬件层                                     │
│   NVIDIA / AMD GPU  ·  温度传感器  ·  散热/冷却回路            │
└─────────────────────────────────────────────────────────────┘
```

## 运行模式

`DVFSController` 提供 5 种模式，通过 `--mode` 或 `set_power_mode()` 选择：

| 模式 | 常量 | 策略 | 适用场景 |
|---|---|---|---|
| `max` | `MAX_PERFORMANCE` | 功耗上限设为最大、频率设为最高档 | 峰值性能优先，能效次要 |
| `balanced` | `BALANCED` | 约 75% 功耗上限 + 中高档频率 | 默认折中，适合多数训练/推理 |
| `save` | `POWER_SAVE` | 最低功耗 + 最低频率 | 空闲/低载、节能为主 |
| `optimal` | `ENERGY_OPTIMAL` | 由 ML 模型或启发式选择能效最优频率 | **推荐**，兼顾吞吐与能耗 |
| `thermal` | `THERMAL_AWARE` | 接近峰值温度时逐级降频降功耗 | 高热密度环境，防热降频 |

> 各模式的功耗/频率上限可在 [`configs/gear_config.yaml`](software/configs/gear_config.yaml) 中调整，或用 `--power-limit` / `--clock-limit` 在命令行覆盖。

## 安装

```bash
# 克隆后
cd gear-gpu-runtime

# 安装运行依赖（真实硬件需要 pynvml；纯模拟演示可省略）
pip install -r requirements.txt

# 安装开发/测试依赖
pip install -e ".[dev]"       # pytest / ruff / mypy
```

**依赖说明**：

| 依赖 | 用途 | 缺失时行为 |
|---|---|---|
| `nvidia-ml-py3` (pynvml) | 读取/写入 NVIDIA GPU 状态 | 自动降级为模拟，`--simulate` 可跑 |
| `numpy` | ML 特征向量 | 自动降级为启发式调频 |
| `scikit-learn` / `joblib` | 加载能效预测模型 | 跳过 ML，退回启发式 |
| `pyyaml` | 读取 `gear_config.yaml` | 用默认配置兜底 |
| `pytest` | 单元测试 | 仅开发需要 |

## 快速开始

**① 纯软件模拟（无需 GPU，推荐先跑通）**

```bash
cd software
python main.py --simulate --mode optimal
```

**② 单帧预览（截图 / CI / 快速验证）**

```bash
python main.py --simulate --mode optimal --once
```

**③ 真实硬件（NVIDIA + pynvml）**

```bash
python main.py --mode thermal --gpu 0
python main.py --mode max --power-limit 250
python main.py --mode optimal --clock-limit 1800
```

**④ 一行功耗优化**

```bash
python -c "from core.power_optimizer import optimize_gpu; print(optimize_gpu())"
```

**⑤ 训练成本估算**

```bash
python scripts/estimate_cost.py --params 671 --tokens 14800 --gpu H100
```

**⑥ 基准测试**

```bash
python scripts/run_benchmark.py
```

## CLI 参考

`python main.py [options]`

| 选项 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--mode` | `max`/`balanced`/`save`/`optimal`/`thermal` | `optimal` | 运行模式 |
| `--gpu` | int | `0` | GPU 索引 |
| `--power-limit` | float | — | 覆盖功耗封顶 (W) |
| `--clock-limit` | int | — | 覆盖频率封顶 (MHz) |
| `--simulate` | flag | off | 强制使用模拟传感器 |
| `--once` | flag | off | 只打印一帧后退出 |

## 模块 API 参考

### `core/dvfs_controller.py`

```python
from core.dvfs_controller import DVFSController, PowerMode

ctrl = DVFSController(gpu_index=0, config={})

ctrl.set_power_limit(250)        # 功耗封顶 (W)，夹到硬件约束
ctrl.set_clock_limit(1800)       # 频率封顶 (MHz)，吸附到最近档位
ctrl.set_power_mode(PowerMode.ENERGY_OPTIMAL)  # 切换模式

ctrl.update_state()              # 采集最新状态
ctrl.predict_optimal_frequency()  # ML/启发式预测最优频率
ctrl.get_energy_report()         # 温度/功耗/频率/能耗/热状态报告

ctrl.start()                     # 启动后台控制线程
ctrl.stop()                      # 停止
```

**关键属性/常量**：`state`（`GPUState`：temperature/power_usage/core_clock/utilization/energy_total）、`freq_table`、`ALPHA`/`BETA`（`P ≈ α·f^β`）、`TEMP_ASSERT=83`、`TEMP_CRITICAL=90`。

### `core/thermal_manager.py`

```python
from core.thermal_manager import ThermalManager

th = ThermalManager()
th.update_thermal_state(78)      # 更新热状态
th.thermal_guidance()            # 返回状态 + 降频/降功耗建议
th.control_coolant_flow(70)      # 简化 PID 冷却流控
th.start_monitoring(cb)          # 启动监控线程
th.stop_monitoring()
```

**热状态分级**：`COOL(<55)` / `NOMINAL(55-72)` / `WARM(72-83)` / `HOT(83-90)` / `CRITICAL(>90)`。

### `core/power_optimizer.py`

```python
from core.power_optimizer import GPUPowerOptimizer, optimize_gpu

optimize_gpu()                   # 一行优化
GPUPowerOptimizer().apply_energy_saver()   # 节能档
```

## 配置参考

[`software/configs/gear_config.yaml`](software/configs/gear_config.yaml)：

```yaml
system:
  sampling_interval_ms: 200      # 控制循环采样周期
gpu:
  power_limits_w: {min: 30, max: 300}   # 按实际 GPU 调整
  clock_limits_mhz: {min: 300, max: 2100}
modes:
  max_performance: {power_limit_pct: 100, clock_target: max}
  balanced:        {power_limit_pct: 75,  clock_target: auto}
  power_save:      {power_limit_pct: 50,  clock_target: min}
  energy_optimal:  {power_limit_pct: auto, clock_target: ml}
  thermal_aware:   {temp_assert_c: 83, temp_critical_c: 90}
thermal:
  baseline_recover_c: 40          # 高于此温才算可回收废热
  heat_recovery_efficiency: 0.85
ml_model:
  model_path: models/rf_power_model.joblib
  features: [utilization, occupancy, power, temperature]
```

## ML 能效预测

当 `models/rf_power_model.joblib` 存在时，`DVFSController` 会用它预测能效最优频率；否则退回基于利用率的启发式规则。

- **输入特征**：`[utilization, sm_occupancy, power, temperature]`
- **模型**：`RandomForest` / `XGBoost` 回归（`predict` 输出频率）
- **训练数据**：用 `scripts/run_benchmark.py` 在不同频率/负载下采集（频率、功耗、利用率、温度、吞吐），以"单位能耗吞吐最高"为标签训练。

**为何用 ML 而非固定公式**：GPU 的功耗-频率关系受工艺、温度、工作负载与指令混合影响，偏离 `P ≈ α·f^β` 的简单幂律；ML 能在特征空间上更贴近真实 Pareto 前沿。

## 评估方法论

**要做的**：在真实 GPU 上，用统一协议对比"基线策略 vs GEAR 策略"，量化能效收益。

**基准负载**：LLM 推理（vLLM）、MLPerf、HPC kernels（如 CUDA 示例）、训练 step。

**核心指标**：

| 指标 | 定义 | 关注点 |
|---|---|---|
| `perf-per-watt` | tokens/s ÷ W（或 FLOPS/W） | 单位功耗吞吐 |
| `Energy-Delay Product` | 能耗 × 时间 | 综合能效与延迟 |
| 峰值功耗 | 运行期间最大功率 | 供电/散热预算 |
| p99 延迟 | 延迟尾部分位数 | 服务质量 |
| 功耗封顶达成率 | 是否稳定在目标上限内 | 约束有效性 |

**对照实验**：

1. 基线（不作任何控制）；
2. 仅功耗封顶；
3. 启发式 DVFS；
4. ML 预测 DVFS（本系统）。

**结论标准**：只有当实测结果出来后，才能在 README / 报告中写明"降低 X%"等量化结论；**未实测前不做未经验证的宣称**。

## 校准

`P ≈ α · f^β` 中的 `ALPHA` / `BETA` 与 GPU 强相关，必须实测拟合：

```bash
python scripts/calibrate.py
```

它会用一组 `(频率, 功耗)` 样本，在对数空间做线性回归得到 `β` 与 `α`。把结果写回 `DVFSController.ALPHA/BETA` 后，功耗估计与最优频率预测会更准。

> 示例脚本默认用演示数据；请用真实 GPU 测量值替换。

## 测试

```bash
pytest -q                          # 运行全部单元测试
python -m py_compile software/core/*.py software/main.py scripts/*.py
```

测试覆盖：频率档位、功耗封顶夹取、频率吸附、启发式调频、模式切换、热状态分级、可回收废热边界、降频建议。

## 项目结构

```
gear-gpu-runtime/
├── README.md                       # 本文档
├── LICENSE.md                      # MIT
├── pyproject.toml                  # 元数据 / ruff / mypy / pytest
├── requirements.txt                # 运行依赖
├── .github/workflows/ci.yml        # CI：lint + test + compile
├── software/
│   ├── main.py                     # CLI 遥测仪表盘
│   ├── __init__.py
│   ├── core/
│   │   ├── dvfs_controller.py       # DVFS + 功耗封顶 + ML 调频
│   │   ├── thermal_manager.py       # 热管理 + 可回收废热
│   │   └── power_optimizer.py       # 通用功耗优化
│   └── configs/
│       └── gear_config.yaml         # 系统配置
├── scripts/
│   ├── calibrate.py                 # 实测拟合 P≈α·f^β
│   ├── run_benchmark.py             # 基准测试
│   └── estimate_cost.py             # 训练成本估算
├── tests/
│   ├── test_dvfs.py
│   └── test_thermal.py
└── models/                          # ML 能效模型占位
    └── .gitkeep
```

## 路线图

- [ ] 真实 GPU 基准与能效报告（`perf-per-watt`、EDP）
- [ ] ML 模型训练与在线更新
- [ ] AMD ROCm 完整适配
- [ ] 遥测导出（Prometheus）
- [ ] 系统守护（systemd / Docker）
- [ ] 多 GPU 集群级能耗调度

## 贡献

欢迎 PR。请：

1. Fork 并新建分支；
2. 保持代码风格（见 `pyproject.toml` 的 `ruff` 配置）；
3. 为新增逻辑补充单元测试（不依赖 GPU）；
4. 提交前运行 `pytest`。

## 许可

- 软件：**MIT**（见 [`LICENSE.md`](LICENSE.md)）。

## 安全说明

⚠️ 涉及真实硬件的改频、功耗封顶、温度约束时，请在**受控环境**操作，并遵守厂商规范与数据中心安全规程。过高频率/功率可能导致硬件过热或保护性关机；请勿在无监控、无散热余量或涉及生产业务的设备上草率测试。

## FAQ

**Q：没有 NVIDIA GPU 能跑吗？**
A：能。`--simulate` 会使用模拟传感器；缺 `pynvml` 时也会自动降级。适合演示与 CI。

**Q：为什么 `perf-per-watt` 在模拟模式下显示的是占位值？**
A：因为缺少真实吞吐（tokens/s）。接入真实业务吞吐后该指标才有意义。

**Q：如何得到最准的功耗模型？**
A：用 `scripts/calibrate.py` 在你的 GPU 上实测，写回 `ALPHA/BETA`。

**Q：ML 模型哪里来？**
A：用 `run_benchmark.py` 采集真实数据，以"单位能耗吞吐最高"为标签训练 `RandomForest/XGBoost`，存到 `models/`。
