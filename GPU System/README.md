# ⚙️ GPU System · GEAR（GPU Energy-Aware Runtime）

> 一套面向 GPU 的**能耗感知运行时**：动态电压频率调整（DVFS）、功耗/频率封顶、温度保护与可回收废热度量。
> 目标：**在不损失吞吐的前提下，最小化 GPU 能耗与峰值功耗。**

本目录是 [`Project of ChenShen`](../README.md) 仓库中的一个子项目（原为独立仓库，已并入主仓库）。

**语言** Python 3.9+ · **许可** MIT · **硬件** NVIDIA（NVML）/ AMD（ROCm 适配中）

---

## 功能

| 模块 | 作用 |
|---|---|
| `DVFSController` | 动态调频 + 功耗封顶 + **真正锁频**（`nvidia-smi -lgc`）+ **二维 ML 调频**（计算利用率 × 显存带宽利用率）+ 温度感知降频 |
| `ThermalManager` | 温度采集、热状态分级、过热降频、可回收废热度量 |
| `GPUPowerOptimizer` | 一键保守功耗优化（NVIDIA/AMD），锁频/复位用真实 `-lgc`/`-rgc` |
| `autodl_boot.sh` | **AutoDL 一键采集**：装依赖 → vLLM 拿真实吞吐 → 采功耗 → 算 perf-per-watt → 拟合校准 |
| CLI 遥测仪表盘 | 实时展示温度/功耗/频率/利用率/累计能耗/性能功耗比 |

## 运行模式

| 模式 | 策略 |
|---|---|
| `max` | 跑满，不设限 |
| `balanced` | 75% 功耗 + 中高档频率 |
| `save` | 最低功耗 + 最低频率 |
| `optimal` | **能效最优**：ML/启发式选频 |
| `thermal` | **温度感知**：接近峰值时逐级降频 |

## 快速开始（纯软件模拟，无需 GPU）

```bash
cd software
python main.py --simulate --mode optimal

# 单帧预览（截图/CI）
python main.py --simulate --mode optimal --once

# 真实硬件（NVIDIA + pynvml）
python main.py --mode thermal --gpu 0

# 一行功耗优化
python -c "from core.power_optimizer import optimize_gpu; print(optimize_gpu())"

# 训练成本估算（含 PUE 预设与互联带宽瓶颈）
python scripts/estimate_cost.py --params 671 --tokens 14800 --gpu H100 --dc nmg
# --dc: default(1.30) / nmg(内蒙古天然冷风, 1.15) / zhongguancun(城市机房, 1.70)
# --network-loss: 千卡互联带宽瓶颈导致的等效效率损失(0-1, 默认0.10)
# 显式 --pue 覆盖 --dc：python scripts/estimate_cost.py --gpu H100 --pue 1.7

# 实测功率采集器（能效网格脚本）→ 输出 CSV 功率曲线
python scripts/collect_power.py --simulate --duration 20        # 无 GPU 演示
python scripts/collect_power.py --duration 60 --chart           # 真机采集 + 曲线 PNG
python scripts/collect_power.py --duration 60 --facility-power-w 120000 --it-power-w 40000  # 估算 PUE

# AutoDL 一键：装依赖 → vLLM 拿真实吞吐 → 采功耗 → 算 perf-per-watt → 拟合校准
bash scripts/autodl_boot.sh                                     # 模型/时长可设 MODEL=... DURATION=60
```

安装真实硬件依赖：`pip install -r requirements.txt`（缺 `pynvml` 会自动降级为模拟）。

> 🔒 **关于锁频**：`set_clock_limit` 用底层 `nvidia-smi -lgc` 真正锁定频率区间，而非仅设会被睿频回弹的偏移量；需管理员权限，失败时降级并**明确告警**（不静默）。`predict_optimal_frequency` 为二维启发式：显存忙而计算闲（访存密集）时用低频省电，计算密集时按利用率拉高频率。
>
> 📈 **关于实测与 PUE**：`collect_power.py` 用 NVML 实测 GPU 功耗/温度/频率写入 CSV，供画功率曲线；汇总给出平均/峰值功耗与累计能耗。真实 PUE = 机房总功率 / IT 总功率，脚本无法自行侦测机房侧数据，只能用你传入的 `--facility-power-w` 与 `--it-power-w` 按给定口径计算——**这是估算口径，不据此下能效结论**。接入真实栅格/机房功率读数后即可变成实测 PUE。

> 详细 API/配置/评估方法见 `docs/`（架构/API/设计决策/FAQ）。本目录中 `scripts/` 下有 `calibrate.py`（实测拟合 `P ≈ α·f^β`）、`run_benchmark.py`（基准）、`estimate_cost.py`（训练成本估算）。

## 目录结构

```
GPU System/
├── software/                    # 核心运行时
│   ├── main.py                  # CLI 遥测仪表盘
│   ├── core/dvfs_controller.py  # DVFS + 功耗封顶 + ML 调频
│   ├── core/thermal_manager.py  # 热管理 + 可回收废热
│   ├── core/power_optimizer.py  # 通用功耗优化
│   └── configs/gear_config.yaml # 配置
├── scripts/                     # calibrate / run_benchmark / estimate_cost / collect_power / autodl_boot(一键采集)
├── tests/                       # pytest（无需 GPU/numpy）
├── models/                      # ML 能效模型占位
├── archive/                     # 早期"烤串"玩笑版归档
├── docs/                        # (见仓库 docs/)
├── .github/workflows/ci.yml     # lint + test + compile
├── pyproject.toml · requirements.txt · LICENSE.md
└── README.md
```

## 测试

```bash
pip install -e ".[dev]"    # pytest / ruff / mypy
pytest -q                  # 单测（零 GPU / 零三方依赖）
ruff check software tests
```

## 为什么值得做

训练/推理的 GPU 账单是数据中心最大开销之一（例如 DeepSeek-V3 约 $5.6M 算力成本）。通过功耗封顶 + DVFS，**理论上限**可降低 20–30% 能耗——这是**潜力上限，未经本仓库实测验证**。当前 README 不含任何未经验证的"降低 X%"承诺性声明；具体幅度以 `scripts/collect_power.py` 在真实硬件上采集的数据为准。

## 许可

MIT（见 [`LICENSE.md`](LICENSE.md)）。

---

> ⚠️ 说明：涉及真实硬件的调频/封顶请在受控环境操作，遵守厂商与数据中心规范。
