#!/bin/bash
# Raft 分布式 KV + 故障转移 完整测试
# 用实时 status 查询确认当前 Leader（避免日志猜错）
cd "$(dirname "$0")"

PEERS=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102

echo "== cleanup =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1
rm -f raft_*.json node*.log

echo "== start 3 nodes =="
coproc N0 { ./build/raft_node.exe --id=0 --peers=$PEERS > node0.log 2>&1; }
coproc N1 { ./build/raft_node.exe --id=1 --peers=$PEERS > node1.log 2>&1; }
coproc N2 { ./build/raft_node.exe --id=2 --peers=$PEERS > node2.log 2>&1; }
NCMD[0]=${N0[1]}; NCMD[1]=${N1[1]}; NCMD[2]=${N2[1]}
NPID[0]=$N0_PID;  NPID[1]=$N1_PID;  NPID[2]=$N2_PID

# 向每个节点发 status，看它当前角色，返回当前 Leader（谁的最近 role 是 LEADER）
current_leader() {
  for i in 0 1 2; do echo "status" >&${NCMD[$i]}; done
  sleep 1
  for i in 0 1 2; do
    last=$(grep -o "role=[A-Z]*" node$i.log | tail -1)
    if [ "$last" = "role=LEADER" ]; then echo $i; return; fi
  done
  echo -1
}

echo "== wait for a stable leader =="
L=-1
for t in 1 2 3 4 5 6 7 8; do
  sleep 2
  L=$(current_leader)
  if [ "$L" != "-1" ]; then echo "  (t=${t}0s) leader = node $L"; break; fi
done
if [ "$L" = "-1" ]; then
  echo "NO leader elected! Dumping node logs:"
  for i in 0 1 2; do echo "--- node $i (tail) ---"; tail -20 node$i.log; done
  taskkill //F //IM raft_node.exe 2>/dev/null; exit 1
fi
echo ">> CURRENT LEADER = node $L"

echo "== set foo bar on leader =="
echo "set foo bar" >&${NCMD[$L]}
sleep 2
echo "== check APPLY on all nodes =="
for i in 0 1 2; do
  grep -q "APPLY set foo = bar" node$i.log && echo "node $i: foo=bar APPLIED" || echo "node $i: NOT applied"
done
echo "== leader($L) set response =="
grep -E "OK set|ERROR|APPLY" node$L.log | tail -3

echo "== get foo on a follower =="
F=0; [ "$F" = "$L" ] && F=1
echo "get foo" >&${NCMD[$F]}
sleep 1
echo "  (follower node $F log:)"; grep -E "foo = |OK|ERROR" node$F.log | tail -2

echo "== KILL leader node $L =="
kill -9 ${NPID[$L]} 2>/dev/null || taskkill //F //PID ${NPID[$L]}
echo "killed, waiting for failover..."
sleep 10
L2=$(current_leader)
if [ "$L2" = "-1" ]; then echo "!! no new leader after failover"; else echo ">> NEW LEADER = node $L2"; fi

echo "== set baz qux on new leader =="
echo "set baz qux" >&${NCMD[$L2]}
sleep 2
for i in 0 1 2; do
  grep -q "APPLY set baz = qux" node$i.log && echo "node $i: baz=qux APPLIED" || echo "node $i: baz=qux not applied"
done
echo "== new leader($L2) set response =="
grep -E "OK set|ERROR|APPLY" node$L2.log | tail -3

echo "== stop =="
taskkill //F //IM raft_node.exe 2>/dev/null
sleep 1
echo
echo "########## role transitions ##########"
for i in 0 1 2; do
  echo "--- node $i ---"
  grep -E "became (LEADER|CANDIDATE|FOLLOWER)" node$i.log | tail -6
done
echo "########## APPLY log ##########"
for i in 0 1 2; do
  echo "--- node $i ---"
  grep "APPLY set" node$i.log
done
