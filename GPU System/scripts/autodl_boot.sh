#!/usr/bin/env bash
#
# GEAR · AutoDL 一键数据采集（并行版）
# 正确做法：让 vLLM 压测【与】功耗采集【同时】进行，否则功耗落到空闲上，perf-per-watt 失真。
#
# 用法： bash scripts/autodl_boot.sh
# 可选环境变量：MODEL / DURATION / OUT / NUM_PROMPTS / REQUEST_RATE / LOAD_WAIT / HF_ENDPOINT
set -u

PY=python3; command -v "$PY" >/dev/null 2>&1 || PY=python
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="${MODEL:-Qwen/Qwen2-7B-Instruct}"
DURATION="${DURATION:-40}"
INTERVAL="${INTERVAL:-1.0}"
OUT="${OUT:-p_load.csv}"
NUM_PROMPTS="${NUM_PROMPTS:-100}"
REQUEST_RATE="${REQUEST_RATE:-10}"
LOAD_WAIT="${LOAD_WAIT:-60}"              # 等模型下载/加载的秒数
REQ_LOG="${OUT%.csv}_perf.log"

echo "==> 依赖（pynvml 读功耗）..."
"$PY" -m pip install --quiet nvidia-ml-py3 numpy 2>&1 | tail -2 || true
"$PY" -c "import vllm" 2>/dev/null || echo "⚠️ 无 vllm，仅采功耗曲线；吞吐需手动填。"

echo "==> 后台起 vLLM 压测 ($MODEL) ..."
[ -n "${HF_ENDPOINT:-}" ] && export HF_ENDPOINT="$HF_ENDPOINT"
nohup "$PY" -m vllm.benchmark.benchmark_serving \
      --model "$MODEL" --backend vllm \
      --num-prompts "$NUM_PROMPTS" --request-rate "$REQUEST_RATE" \
      > "$ROOT/$REQ_LOG" 2>&1 &

echo "==> 等待模型加载 ${LOAD_WAIT}s ..."
sleep "$LOAD_WAIT"
echo "   （vllm 日志末尾：）"; tail -3 "$ROOT/$REQ_LOG"

echo "==> 并行采集功耗 ${DURATION}s ..."
"$PY" "$ROOT/scripts/collect_power.py" --duration "$DURATION" --interval "$INTERVAL" \
      --out "$ROOT/$OUT"

echo "==> 等待压测结束，读取吞吐 ..."
wait
TPS="$(grep -iE 'Throughput' "$ROOT/$REQ_LOG" | grep -oiE '[0-9]+(\.[0-9]+)?' | tail -1)" || true

# 从 CSV 汇总读平均功耗
AVG_POWER="$("$PY" - "$ROOT/$OUT" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
p = [float(r["power_w"]) for r in rows]
print(round(sum(p) / len(p), 1) if p else "0")
PY
)"

echo "=========================================================="
echo "  平均功耗     : ${AVG_POWER} W"
if [ -n "$TPS" ] && [ "${TPS%%.*:-0}" -gt 0 ] 2>/dev/null; then
  PERF="$(awk "BEGIN{printf \"%.3f\", $TPS / $AVG_POWER}")"
  echo "  吞吐         : ${TPS} token/s"
  echo "  性能功耗比   : ${PERF} tok/s/W"
else
  echo "  吞吐         : 未取到（看 $REQ_LOG 的 Throughput 行）"
fi
echo "  CSV          : $ROOT/$OUT"
echo "  vLLM 日志    : $ROOT/$REQ_LOG"
echo "=========================================================="
