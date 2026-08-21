#!/bin/bash
# 一次性自动化 Raft 三节点测试：
#  - 杀掉所有残留 raft_node.exe
#  - 删除持久化任期文件
#  - 用全新端口 8100-8102 启动 3 节点，输出写日志
#  - 跑 25 秒后自动停止，并打印三个日志
cd "$(dirname "$0")"

echo "== 1) kill leftover raft_node.exe =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1
echo "remaining raft processes:"
tasklist | grep -i raft || echo "(none)"

echo "== 2) remove persisted term files =="
rm -f raft_0.json raft_1.json raft_2.json
echo "done"

echo "== 3) start 3 nodes on ports 8100-8102 =="
PEERS=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102
./build/raft_node.exe --id=0 --peers=$PEERS < /dev/null > node0.log 2>&1 &
./build/raft_node.exe --id=1 --peers=$PEERS < /dev/null > node1.log 2>&1 &
./build/raft_node.exe --id=2 --peers=$PEERS < /dev/null > node2.log 2>&1 &

echo "running for 25s..."
sleep 25

echo "== 4) stop =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1

for i in 0 1 2; do
  echo ""
  echo "################ NODE $i ################"
  cat node$i.log
done
