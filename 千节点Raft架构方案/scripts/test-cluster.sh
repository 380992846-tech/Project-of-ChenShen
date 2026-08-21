#!/bin/bash
# scripts/test-cluster.sh
# 冒烟测试：验证集群基本读写功能

set -euo pipefail

ROUTER="${ROUTER_URL:-http://localhost:8080}"
CLIENT_BIN="./kvstore-client"

echo "=== KV 集群冒烟测试 ==="

# 方式一：通过路由层 HTTP 测试
echo ""
echo "--- 1. 通过路由层写入/读取 ---"
KEY="test:hello"
VALUE="world"

curl -s -X PUT -H "Content-Type: application/json" \
    -d "{\"key\":\"$KEY\",\"value\":\"$VALUE\"}" \
    "$ROUTER/api/v1/key/$KEY" > /dev/null

RESULT=$(curl -s "$ROUTER/api/v1/key/$KEY")
echo "GET $KEY => $RESULT"

if [[ "$RESULT" != *"$VALUE"* ]]; then
    echo "FAIL: 读取结果未包含预期值"
    exit 1
fi

echo "PASS: 读写正常"

# 方式二：通过客户端 SDK 测试（如果编译了）
echo ""
echo "--- 2. 通过客户端 SDK 测试 ---"
if [[ -x "$CLIENT_BIN" ]]; then
    "$CLIENT_BIN" get test:hello
    "$CLIENT_BIN" set test:world kvstore
else
    echo "SKIP: 未找到 kvstore-client (可执行: go run ./cmd/kvstore-client)"
fi

# 方式三：压力小样本
echo ""
echo "--- 3. 小样本并发写入 ---"
for i in $(seq 1 10); do
    curl -s -X PUT -H "Content-Type: application/json" \
        -d "{\"key\":\"bench:$i\",\"value\":\"v$i\"}" \
        "$ROUTER/api/v1/key/bench:$i" > /dev/null &
done
wait

COUNT=0
for i in $(seq 1 10); do
    R=$(curl -s "$ROUTER/api/v1/key/bench:$i")
    [[ "$R" == *"v$i"* ]] && COUNT=$((COUNT+1))
done
echo "写入/读取一致数: $COUNT/10"

echo ""
echo "=== 测试完成 ==="
