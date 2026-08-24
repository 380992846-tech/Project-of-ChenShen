#!/usr/bin/env bash
#
# GEAR · AutoDL 一键数据采集
# 在 AutoDL（或任何有 NVIDIA GPU 的 Linux 容器）上运行：
#   bash scripts/autodl_boot.sh
#
# 一键完成：
#   1) 装依赖（pynvml / numpy / matplotlib / vllm）
#   2) 用 vLLM 压测一个小模型，拿到【真实吞吐 tokens/s】
#   3) 同步用 collect_power.py 采集【真实功耗/温度/频率曲线】
#   4) 自动算 perf-per-watt（tokens/s/W）并落 CSV + PNG
#   5) 用真实数据拟合 ALPHA/BETA（写回 dvfs_controller 用）
#
# 可选环境变量（默认值见下）：
#   MODEL   = Qwen/Qwen2-7B-Instruct   # 单卡装得下的模型即可
#   DURATION= 60                       # 采集秒数
#   OUT     = p_curve.csv              # 输出 CSV
#   USE_VLLM= 1                        # 0 则跳过 vLLM，纯采功耗曲线
#   HF_ENDPOINT= https://hf-mirror.com # 国内拉模型加速（可选）
set -u

PY=python3; command -v "$PY" >/dev/null 2>&1 || PY=python
ROOT="$(cd "$(dirname "$0")/.." && pwd)"     # GPU System 目录
MODEL="${MODEL:-Qwen/Qwen2-7B-Instruct}"
DURATION="${DURATION:-60}"
INTERVAL="${INTERVAL:-1.0}"
OUT="${OUT:-p_curve.csv}"
USE_VLLM="${USE_VLLM:-1}"
REQ_RATE="${REQUEST_RATE:-10}"
NPROMPTS="${NUM_PROMPTS:-200}"

echo "=========================================================="
echo "  GEAR · AutoDL 采集  (模型=$MODEL, 时长=${DURATION}s)"
echo "=========================================================="

# ---- 0) 检查 NVIDIA 环境 ----
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "⚠️  未检测到 nvidia-smi，请确认已租用带 GPU 的实例。"
fi
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || true

# ---- 1) 依赖 ----
echo "==> 安装依赖 ..."
"$PY" -m pip install --quiet nvidia-ml-py3 numpy matplotlib 2>&1 | tail -2 || echo "⚠️ 依赖安装有警告，继续。"

# ---- 2) vLLM 压测拿真实吞吐 ----
TPS=""
if [ "$USE_VLLM" = "1" ]; then
  echo "==> 安装 vLLM（较大，可能几分钟）..."
  "$PY" -m pip install --quiet vllm 2>&1 | tail -3 || echo "⚠️ vLLM 安装失败，将跳过吞吐测试。"
  if "$PY" -c "import vllm" 2>/dev/null; then
    echo "==> 起 vLLM 压测 ($MODEL ...) 拿吞吐 ..."
    export HF_HUB_ENABLE_HF_TRANSFER=0
    [ -n "${HF_ENDPOINT:-}" ] && export HF_ENDPOINT="$HF_ENDPOINT"
    TPS="$("$PY" -m vllm.benchmark.benchmark_serving \
           --model "$MODEL" --num-prompts "$NPROMPTS" --request-rate "$REQ_RATE" 2>/dev/null \
           | grep -iE 'Throughput|tokens/s' | grep -oE '[0-9]+(\.[0-9]+)?' | tail -1)" || true
    echo "测得真实吞吐: ${TPS:-未知} token/s"
  fi
fi

# ---- 3) 采集功耗曲线 ----
echo "==> 采集真实功耗/温度/频率 (${DURATION}s) ..."
CHART_OPT=""
"$PY" -c "import matplotlib" 2>/dev/null && CHART_OPT="--chart"
if [ -n "$TPS" ]; then
  "$PY" "$ROOT/scripts/collect_power.py" --duration "$DURATION" --interval "$INTERVAL" \
        --throughput "$TPS" $CHART_OPT --out "$ROOT/$OUT"
else
  echo "   （无真实吞吐，本次为纯功耗曲线；perf-per-watt 需加 --throughput）"
  "$PY" "$ROOT/scripts/collect_power.py" --duration "$DURATION" --interval "$INTERVAL" \
        $CHART_OPT --out "$ROOT/$OUT"
fi

# ---- 4) 校准 ALPHA/BETA ----
if [ -s "$ROOT/$OUT" ]; then
  echo "==> 用真实数据拟合 P≈α·f^β ..."
  "$PY" "$ROOT/scripts/calibrate.py" --csv "$ROOT/$OUT" || true
fi

echo "=========================================================="
echo "  完成 ✅  曲线: $ROOT/$OUT"
echo "  图表: ${OUT%.csv}.png  （若装了 matplotlib）"
echo "  下一步: 把 CSV/PNG 拉到本地，或直接贴进 README。"
echo "=========================================================="
