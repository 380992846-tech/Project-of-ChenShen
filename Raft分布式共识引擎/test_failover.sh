#!/bin/bash
# Raft Leader 故障转移测试：
#  1) 启动 3 节点，等出 Leader
#  2) 杀掉当前 Leader
#  3) 观察剩余节点自动重新选举出新 Leader
cd "$(dirname "$0")"

PEERS=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102

echo "== cleanup =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1
rm -f raft_*.json node*.log node*.pid

echo "== start 3 nodes =="
for i in 0 1 2; do
  ./build/raft_node.exe --id=$i --peers=$PEERS < /dev/null > node$i.log 2>&1 & echo $! > node$i.pid
done

# 找出当前 Leader（日志里第一个打出 "became LEADER" 的节点）
leader() {
  for i in 0 1 2; do
    if grep -q "became LEADER" node$i.log; then echo $i; return; fi
  done
  echo -1
}

echo "== waiting for initial leader =="
sleep 6
L=$(leader)
if [ "$L" = "-1" ]; then
  echo "NO leader elected! check logs"; taskkill //F //IM raft_node.exe 2>/dev/null; exit 1
fi
echo ">> INITIAL LEADER = node $L  (term=$(grep -o 'Term=[0-9]*' node$L.log | tail -1))"

echo "== KILL leader node $L =="
kill -9 $(cat node$L.pid) 2>/dev/null || taskkill //F //PID $(cat node$L.pid)
echo "killed node $L, waiting for failover..."
sleep 8

echo "== check remaining nodes for new leader =="
L2=-1
for i in 0 1 2; do
  [ "$i" = "$L" ] && continue
  if grep -q "became LEADER" node$i.log; then
    echo ">> NODE $i elected LEADER after failover"
    grep -E "became (CANDIDATE|LEADER|FOLLOWER)" node$i.log | tail -4
    L2=$i
  fi
done
if [ "$L2" = "-1" ]; then
  echo "!! No new leader elected (failover FAILED)"
else
  echo ">> FAILOVER SUCCESS: new leader = node $L2"
fi

echo "== stop all =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1
echo "done"
