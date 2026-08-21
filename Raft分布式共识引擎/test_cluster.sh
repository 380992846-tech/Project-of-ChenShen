#!/bin/bash
# 启动3节点集群
for i in 0 1 2; do
    ./raft_node --id=$i --peers="127.0.0.1:9000,127.0.0.1:9001,127.0.0.1:9002" &
done

# 模拟故障
sleep 2
kill -9 $(pgrep -f "raft_node --id=0")  # 杀掉Leader
sleep 5
# 观察日志，应有新Leader选出