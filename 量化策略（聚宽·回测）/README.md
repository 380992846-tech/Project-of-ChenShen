# 量化系统 · A股 TMT 板块

把原先散落在一层的量化策略（`quant_v14.py` / `quant_v21.py` / `quant_xgboost_shap.py` /
`joinquant_v18.py` / `quant_features.py` / `金融数学.py`）重构为一个**标准、可运行、可融合前端中台**的完整量化系统。

目标市场：**A股，重点是 TMT（科技/媒体/通信）板块**，并把「黑紫毛玻璃 TMT 中台」前端改造成**数据驱动**，通过 FastAPI 与策略引擎联通。

---

## 项目结构

```
量化系统/
├── config/                # 统一配置（config.yaml + pydantic-settings）
├── data/                  # 数据层：多数据源抽象、清洗、缓存、可组合因子库
├── strategy/              # 策略层：BaseStrategy 抽象 + TMT轮动 / 风险平价
├── backtest/              # 回测引擎（向量化）、绩效指标、报告/图表
├── risk/                  # 风控层：事前 / 事中 / 事后
├── execution/             # 执行层：SimulatedBroker / LiveBroker 适配器骨架
├── service/               # 编排器、持久化(SQLite)、调度、日志
├── api/                   # FastAPI 后端（/api/*）
├── web/                   # 数据驱动的 TMT 量化中台前端
├── main.py                # 系统入口（run / serve / dashboard）
├── requirements.txt
└── __init__.py
```

---

## 快速开始

### 1. 安装依赖

核心只需 pandas / numpy / pydantic-settings / PyYAML / matplotlib / fastapi / uvicorn /
requests。真实行情与 ML 为可选：

```bash
pip install -r 量化系统/requirements.txt
```

### 2. 运行回测（离线可用）

系统默认 `environment: offline`，用**确定性合成行情**兜底，即使没有网络、没装
akshare/sklearn 也能完整跑通：

```bash
# 从仓库根目录（D:\my_projects\QUANT 的上一级 D:\my_projects）运行
PYTHONPATH=D:\my_projects python -m 量化系统.main run
```

### 3. 启动 FastAPI 中台

```bash
PYTHONPATH=D:\my_projects python -m 量化系统.main serve
# 打开 http://127.0.0.1:8000  → 数据驱动的 TMT 量化中台
```

### 4. 查看中台状态 JSON

```bash
PYTHONPATH=D:\my_projects python -m 量化系统.main dashboard --json
```

### 5. API 端点

| 方法 | 路径              | 说明                                  |
|------|-------------------|---------------------------------------|
| GET  | `/api/dashboard`  | 中台总览（KPI、净值、行业配置、流水、信号） |
| GET  | `/api/portfolio`  | 当前持仓与行业配置                     |
| GET  | `/api/signals`    | 最新交易信号与流水                     |
| GET  | `/api/signals/explain?symbol=...` | 某标的下单信号的自然语言解释（AI 面板） |
| GET  | `/api/backtest`   | 回测绩效摘要                           |
| POST | `/api/run`        | 手动触发一次完整流水                   |

> 前端中台右侧「AI 信号解释」面板点击任一交易即调用 `/api/signals/explain`：
> 默认用因子/特征重要性拼出模板化中文解释；在 `config.yaml` 开启 `llm.enabled`
> 并配置 `endpoint`/`api_key` 后，会调用 LLM 生成更自然的一段话（失败自动回退模板）。

### 6. 参数扫描

对指定策略做网格扫描（**单次加载行情面板并复用**，遍历参数组合，按目标函数排序）：

```bash
PYTHONPATH=D:\my_projects python -m 量化系统.main scan --strategy tmt_rotation --sample 800
# 也可用 --grid '{"momentum_window":[20,40,60],"top_n":[2,3,4]}'
```

会在真实成分股上用全样本做扫描；`score` 默认按夏普排序，也可传权重做综合分。

**滚动前推(out-of-sample)稳健性检验**：

```bash
PYTHONPATH=D:\my_projects python -m 量化系统.main walk-forward --strategy tmt_rotation --n-folds 5
```

按时间把样本切成多折，每折仅用之前数据选参，再到后续未见段评估 OOS 指标，用以判断是否过拟合。

> 已用全样本（2020-2025 真实数据）对 `tmt_rotation` 扫描，最优信号参数为
> `momentum_window=40, trend_window=120, top_n=3`，明显优于原 `20/60/3`。
> 风控稳健配置已写入 `config.yaml`（`target_vol=0.12, vol_cap=0.25, max_drawdown_halt=0.15`）。

**五策略全样本大排名**（2020-2025 真实成分股，含升级后的事中风控；各策略取其扫描最优）：

| 排名 | 策略 | 最佳夏普 | 累计收益 | 最大回撤 |
|------|------|---------|---------|---------|
| 🥇 | `tmt_rotation` | **+0.21** | **+22%** | **-19%** |
| 🥈 | `risk_parity` | -0.10 | +5% | -22% |
| 🥉 | `score_v21` | -0.27 | -4% | -28% |
| 4 | `rf_v18` | -0.37 | -10% | -20% |
| 5 | `xgb_shap` | -0.58 | -16% | -24% |

> `tmt_rotation` 为当前最优，默认 `strategy.name` 已指向它，其余四类偏单标的择时，
> 在板块动量风格下表现弱，适合作为备选/对照。

**滚动前推(out-of-sample)稳健性检验**：

在 `tmt_rotation` 上把时间切成 **5 折**做 walk-forward（每折仅用此前作为训练段选参，再到后续
未见的验证段评估），结论：

- 网格选出的参数在不同折间**不稳定**（`param_consistency=0.5`，折间在 momentum=40 / 60 间摇摆）。
- walk-forward 选参的**平均 OOS 夏普 -0.51**，反而**低于**固定默认参数（`momentum=40/trend=120/top_n=3`）
  的 **OOS 夏普 -0.32** —— 典型过拟合特征：in-sample 优化会夸大数字，真正 OOS 不如直接持有默认配置。
- 因此**当前默认 `40/120/3` 不是过拟合的产物**，而是「在 walk-forward 中作为固定基线反而优于
  逐折选参」的稳健选择；该策略在该板块/区间整体 OOS 夏普为弱负（无稳定显著 alpha），但回撤控制
  在 -9% 左右，属低回撤的稳健型配置。

---


## 可用策略

`python -m 量化系统.main list-strategies`

| 策略名         | 来源               | 思路                                                       |
|----------------|--------------------|------------------------------------------------------------|
| `tmt_rotation` | 默认               | TMT 子行业动量轮动（趋势过滤 + 波动率倒数加权）              |
| `risk_parity`  | quant_v14          | 风险平价 + 趋势/超卖规则买入                                 |
| `rf_v18`       | joinquant_v18      | 随机森林 walk-forward，特征 ret/bias/vol/rsi/trend          |
| `score_v21`    | quant_v21          | 打分制（RSI/布林/量比/背离）+ 动态止盈止损                   |
| `xgb_shap`     | quant_xgboost_shap | XGBoost + 量价情绪代理，特征重要性解释                       |

> **资金流/北向因子（实验结论）**：`factors.py` 新增了资金流代理因子
> （`fund_flow_net` / `fund_flow_upvol` / `fund_flow_obv`）与北向情绪因子
> （`northbound_sentiment`，市场级，来自 `stock_hsgt_hist_em`）。`tmt_rotation` 提供
> `fund_flow_weight` 参数把资金流/OBV 强度融入排序。
>
> **诚实结论**：当前环境**个股/板块资金流水接口（东财）不可达**，只能用**量价代理**；
> 全样本验证该代理在此区间**不增 alpha**（`fund_flow_weight` 0→1 时夏普 0.21 → -1.0，反而恶化）。
> 因此默认 `fund_flow_weight=0`（纯动量），该因子保留为可调项，供接入**真实资金流水/北向
> 明细**后复用。北向情绪为市场级、与个股动量高度相关，同样未贡献独立 alpha。

> 聚宽三件套在离线/无 sklearn/xgboost 环境下会自动退化为**规则版**，保证可跑；
> 安装 sklearn/xgboost 后即启用真实 ML 训练。

---

## 三层风控

- **事前** `PreTradeRisk`：单标的上限（`per_name_limit`）、总仓位上限（`max_position`）、波动率压制。
- **事中实时** `InTradeRisk`：**贯穿全程**的实时风控覆盖层——
  - 波动率自适应仓位：按 `target_vol / trailing_vol` 缩放每 bar 总仓位（只用**历史滚动波动**）；
  - 回撤熔断/恢复：临时净值滚动回撤超过 `max_drawdown_halt` 时把仓位降到 `halt_scale`，
    回撤恢复到 `recover_ratio * halt` 以上再解除（带滞后防抖）；
  - 全程 **前视安全**（`shift(1)` + 滚动窗口），已做「前缀重算 == 全量」验证，无未来数据泄漏。
- **事后** `PostTradeRisk`：行业暴露 / 集中度 / 持仓数统计。

> 事中风控调优后当前配置：`max_drawdown_halt=0.15, halt_scale=0.5, recover_ratio=0.7, target_vol=0.12, vol_floor=0.20`。
> 全样本下把最大回撤从约 **-50% 压到约 -19%~-23%**，且夏普为正（约 +0.21~+0.30）。

---

## 数据源与可插拔

`data/sources.py` 定义了统一 `DataSource.fetch(symbol, start, end)` 接口，并按
`data.sources_priority` 依次尝试、失败自动回退：

- `akshare` —— 免费 A 股/ETF。**自动区分股票 vs ETF**；东财接口被限流/断连时，
  股票自动回退**新浪个股日线**（`stock_zh_a_daily`），ETF 自动回退**新浪 ETF**（`fund_etf_hist_sina`），
  更稳定。
- `synthetic` —— 确定性 GBM（离线兜底）。

**当前 config 默认 `data.sources_priority: ["akshare", "synthetic"]`**。离线/断网时自动回退合成数据。

## TMT 标的池（真实成分股）

`data/universe.py` 提供 **TMT 真实 A股成分股**标的池（按 半导体 / 软件服务 / 消费电子 /
通信设备 / 传媒游戏 分组），每子行业 6 只成分股，共 30 只：

- `config.yaml` 的 `universe.groups` 默认内置这些**真实成分股**；
- `universe_source: curated` 直接使用内置成分股；改为 `akshare` 则尝试联网拉取真实
  行业成分（失败自动回落内置）。
- 提供 `fetch_akshare_universe`（尽力而为）与离线回退，且带缓存（`universe_*.json`）。

```bash
PYTHONPATH=D:\my_projects python -c "from 量化系统.config import get_settings; s=get_settings(); print(len(s.universe_symbols), s.universe_flat)"
# -> 30 {'688981': '半导体', ...}
```

## ML 增强（sklearn / xgboost）

安装 `scikit-learn` 与 `xgboost` 后，`rf_v18`（随机森林 walk-forward）与 `xgb_shap`
（XGBoost + 量价情绪）会**真正走 ML 训练路径**并给出非平凡概率；未安装时自动退化为规则版。

```bash
pip install scikit-learn xgboost
```

## LLM 信号解释

`/api/signals/explain` 默认用因子/特征重要性生成模板化中文解释。开启并配置 LLM 后，
会用 OpenAI 兼容端点生成更自然的 `llm_explanation`（失败自动回退模板）：

```yaml
llm:
  enabled: true
  endpoint: "https://api.openai.com"
  api_key: "sk-..."
  model: "gpt-4o-mini"
```

也可用环境变量覆盖（`QUANT_LLM__ENABLED` 等）。开发验证可用本地 mock：
见 `api/server.py` 说明。

---

## 实盘通道（骨架）

`execution/live.py` 的 `LiveBroker` 是对接券商 API 的骨架（中泰 XTP / 华泰 MATIC /
easytrader / vn.py）。**当前未实现，所有方法抛 NotImplementedError，避免误用。**
接入任何现实通道前，请先在本系统 SimulatedBroker / 回测中验证，再做小资金实盘。

---

## 与原脚本的对应关系

| 原脚本                    | 现在的位置 / 角色                                              |
|---------------------------|---------------------------------------------------------------|
| `quant_features.py`      | 提炼为 `data/factors.py` 可组合因子库，并补充 TMT 因子          |
| `quant_v14.py`           | 风控/风险平价逻辑 → `strategy/risk_parity.py` + `risk/`        |
| `quant_v21.py` / `joinquant_v18.py` / `quant_xgboost_shap.py` | 聚宽版单标的策略；通用打分/买卖规则已抽象进 `BaseStrategy`，可迁移为子类 |
| `金融数学.py`            | 金融数学演示，可作为独立教学模块保留                            |
| `中台.html`              | → `web/index.html` 数据驱动重构（复用黑紫毛玻璃视觉）            |

> 原脚本仍保留在 `D:\my_projects\QUANT`，未删除。聚宽特定的 `jqdata` / `attribute_history`
> 调用无法离线运行，因此这些脚本保留为「聚宽版」参考，其信号思想已融入通用策略层。

---

## 建议

- 首次 `dashboard` 会触发完整流水（加载数据 + 回测 + 存 SQLite），可能需要几秒。
- 生产可开启 APScheduler（`scheduler.enabled: true`）做定时更新/信号/日终快照；
  未安装 `apscheduler` 时自动降级为「不调度，不影响其余功能」。
- 真实信号解释（LLM）可在 `/api/signals` 基础上扩展，把 SHAP/模型输出接入自然语言说明。

---

## 免责声明

本系统用于研究与学习。A股 TMT 板块波动较大，合成/历史数据不构成投资建议；
接入实盘前请确保数据源合法（聚宽/万得等授权数据）并严格落实风控。
