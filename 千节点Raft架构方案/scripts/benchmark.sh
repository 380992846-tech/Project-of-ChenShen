#!/bin/bash
# scripts/benchmark.sh
# 简单性能基准测试

set -euo pipefail

CONCURRENCY=100
OPS=10000
ROUTER="${ROUTER_URL:-http://localhost:8080}"

usage() {
    echo "Usage: $0 [--concurrency N] [--ops N]"
    echo "  --concurrency 并发数 (默认 100)"
    echo "  --ops         总操作数 (默认 10000)"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --concurrency) CONCURRENCY="$2"; shift 2 ;;
        --ops) OPS="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) usage ;;
    esac
done

echo "=== 性能基准测试 ==="
echo "并发数:   $CONCURRENCY"
echo "总操作数: $OPS"
echo ""

START=$(date +%s.%N)

# 生成并发写请求
echo "--- 写入阶段 ---"
for i in $(seq 1 "$OPS"); do
    (
        curl -s -X PUT -H "Content-Type: application/json" \
            -d "{\"key\":\"bench:$i\",\"value\":\"value-$i\"}" \
            "$ROUTER/api/v1/key/bench:$i" > /dev/null
    ) &
    # 控制并发
    if [[ $(( i % CONCURRENCY )) -eq 0 ]]; then
        wait
    fi
done
wait

END=$(date +%s.%N)
ELAPSED=$(echo "$END - $START" | bc)
OPS_PER_SEC=$(echo "scale=0; $OPS / $ELAPSED" | bc)

echo ""
echo "=== 结果 ==="
echo "耗时:       ${ELAPSED}s"
echo "吞吐量:     ${OPS_PER_SEC} ops/s"

# 注：更精确的基准应使用专用工具（如 wrk / hey / ghz）
# 本脚本为并发 HTTP 写的简单示例，实际生产建议使用：
#   hey -n 100000 -c 200 -m PUT -d '{"key":"k","value":"v"}' http://localhost:8080/api/v1/key/k
echo ""
echo "提示: 精确基准建议使用 wrk / hey / ghz 等工具压测"
