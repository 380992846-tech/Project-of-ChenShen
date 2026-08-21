#!/bin/bash
# scripts/start-cluster.sh

set -euo pipefail

# 配置（可通过参数覆盖）
SHARDS=200
NODES_PER_SHARD=5
METADATA_BASE_PORT=2370
DATA_BASE_PORT=8000

usage() {
    echo "Usage: $0 [--shards N] [--nodes-per-shard N] [--test]"
    echo "  --shards          分片数量 (默认 200)"
    echo "  --nodes-per-shard 每分片节点数 (默认 5)"
    echo "  --test            以 2 分片 x 5 节点的小集群启动 (便于本地测试)"
    exit 1
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --shards) SHARDS="$2"; shift 2 ;;
        --nodes-per-shard) NODES_PER_SHARD="$2"; shift 2 ;;
        --test) SHARDS=2; NODES_PER_SHARD=5; shift ;;
        -h|--help) usage ;;
        *) usage ;;
    esac
done

TOTAL_NODES=$((SHARDS * NODES_PER_SHARD))
METADATA_ENDPOINTS="http://localhost:2370,http://localhost:2371,http://localhost:2372,http://localhost:2373,http://localhost:2374"

echo "Starting ${TOTAL_NODES} nodes across ${SHARDS} shards..."

# 1. 启动元数据集群 (etcd)
echo "Starting metadata cluster..."
INITIAL_CLUSTER=""
for i in {0..4}; do
    if [[ $i -gt 0 ]]; then INITIAL_CLUSTER+=","; fi
    INITIAL_CLUSTER+="metadata-$i=http://localhost:238$i"
done

for i in {0..4}; do
    etcd --name metadata-$i \
         --data-dir /tmp/etcd-$i \
         --listen-client-urls "http://localhost:237$i" \
         --advertise-client-urls "http://localhost:237$i" \
         --listen-peer-urls "http://localhost:238$i" \
         --initial-advertise-peer-urls "http://localhost:238$i" \
         --initial-cluster "$INITIAL_CLUSTER" \
         &
done

sleep 5

# 2. 启动所有数据节点
for shard in $(seq 0 $((SHARDS-1))); do
    echo "Starting shard $shard..."
    for node in $(seq 0 $((NODES_PER_SHARD-1))); do
        nodeID="node-${shard}-${node}"
        port=$((DATA_BASE_PORT + shard * 10 + node))
        raftDir="/tmp/raft/${nodeID}"
        mkdir -p "$raftDir"

        # 每个分片第一个节点作为 bootstrap
        BOOTSTRAP_FLAG=""
        if [[ $node -eq 0 ]]; then
            BOOTSTRAP_FLAG="--bootstrap"
        fi

        ./kvstore-node \
            --node-id "$nodeID" \
            --shard-id "$shard" \
            --bind-addr "127.0.0.1:${port}" \
            --raft-dir "$raftDir" \
            --metadata "$METADATA_ENDPOINTS" \
            $BOOTSTRAP_FLAG \
            &
    done
done

echo ""
echo "Cluster started with ${TOTAL_NODES} nodes"
echo "Metadata cluster: http://localhost:2370"
echo "Routing layer:   http://localhost:8080"
echo "Metrics example: http://localhost:9100/metrics"
