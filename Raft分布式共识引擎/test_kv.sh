#!/bin/bash
# Raft 分布式 KV + 故障转移 完整测试
# 用日志确认当前 Leader（避免交互 stdin 在 Windows MSYS2 下的 FIFO/coproc 兼容问题）。
# 启动方式与 test_cluster.sh 一致（< /dev/null），只依赖日志判断，最可靠。
cd "$(dirname "$0")"

PEERS=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102

echo "== cleanup =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1
rm -f raft_*.json node*.log node*.pid

echo "== start 3 nodes =="
for i in 0 1 2; do
  ./build/raft_node.exe --id=$i --peers=$PEERS < /dev/null > node$i.log 2>&1 &
  echo $! > node$i.pid
done

# 用日志找当前 Leader：谁是最近一次 "became LEADER"
leader() {
  for i in 0 1 2; do
    if grep -q "became LEADER" node$i.log; then echo $i; return; fi
  done
  echo -1
}

echo "== wait for a stable leader =="
L=-1
for t in 1 2 3 4 5 6 7 8; do
  sleep 2
  L=$(leader)
  if [ "$L" != "-1" ]; then echo "  (t=${t}0s) leader = node $L"; break; fi
done
if [ "$L" = "-1" ]; then
  echo "NO leader elected! Dumping node logs:"
  for i in 0 1 2; do echo "--- node $i (tail) ---"; tail -20 node$i.log; done
  taskkill //F //IM raft_node.exe 2>/dev/null; exit 1
fi
echo ">> CURRENT LEADER = node $L"

# 显示 leader 的 term 与角色
echo "  leader term: $(grep -o 'Term=[0-9]*' node$L.log | tail -1)"
echo "  leader role: $(grep -o 'role=[A-Z]*' node$L.log | tail -1 || echo '(无 status 输出)')"

echo "== role transitions (all nodes) =="
for i in 0 1 2; do
  echo "--- node $i ---"
  grep -E "became (LEADER|CANDIDATE|FOLLOWER)" node$i.log | tail -5
done

echo "== KILL leader node $L =="
kill -9 $(cat node$L.pid) 2>/dev/null || taskkill //F //PID $(cat node$L.pid) 2>/dev/null
echo "killed node $L, waiting for failover..."
sleep 10

echo "== check remaining nodes for new leader =="
L2=-1
for i in 0 1 2; do
  [ "$i" = "$L" ] && continue
  if grep -q "became LEADER" node$i.log; then
    echo ">> NODE $i elected LEADER after failover"
    L2=$i
  fi
done
if [ "$L2" = "-1" ]; then
  echo "!! No new leader elected (failover FAILED)"
else
  echo ">> FAILOVER SUCCESS: new leader = node $L2"
fi

echo "== stop =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1

# 汇总
echo
echo "########## RESULT ##########"
echo "initial leader: node $L"
echo "post-failover leader: node $L2"
if [ "$L2" != "-1" ]; then echo "VERDICT: PASS (election + failover work)"; else echo "VERDICT: FAIL"; fi
