# C++ 实现的 Raft 分布式共识引擎（+ KV 存储）

> 基于 **C++17 + standalone Asio + nlohmann-json** 从零实现的 Raft 共识模块，支持领导人选举、日志复制、持久化，
> 并在此之上实现了可交互的分布式 KV 存储（set/del/get）与故障转移。

## 核心实现

从零实现 Raft 协议的三大模块：

| 模块 | 实现 |
|------|------|
| **领导人选举** | 随机超时（500–1000ms）+ `RequestVote` RPC + 选举限制（Log Matching Property） |
| **日志复制** | `AppendEntries` + 一致性检查（term + prevLogIndex 校验）+ 冲突条目回退 |
| **持久化** | 当前任期 `term`、投给谁的 `votedFor`、日志元数据落盘到 `raft_<id>.json` |

状态机：`Follower / Candidate / Leader` 三态，`term` 与 `votedFor` 持久化到磁盘，
重启后从持久化状态恢复，不丢失已提交日志。

**KV 状态机**：`apply_command` 把已提交日志应用到 KV store（支持 `set` / `del`），
节点提供交互式命令行 `set <k> <v> | del <k> | get <k> | status | quit`。

## 网络与线程

- **standalone Asio**（`ASIO_STANDALONE`，零 Boost 依赖，CMake 用 FetchContent 自动拉取）；
- 所有 Raft 状态在**单个 io 线程**上由定时器/RPC 回调访问，命令行线程用 `state_mutex_` 串行化，
  加锁顺序统一为 `state_mutex_` -> `kv_mutex_`，避免死锁；
- RPC 消息用 JSON 编解码，4 字节长度前缀 + body 的帧格式。

## 关键问题与解决

- **网络分区场景下旧 Leader 恢复**：旧 Leader 与多数派隔离开时，收到更高 term 的 RPC 响应会立即自增
  `term` 并回退为 `Follower`；通过**任期号（term）递增** + **选举限制（Log Matching Property）**
  保证日志的安全性与一致性，不会覆盖已提交日志；
- **选举活锁**：通过**随机选举超时（500–1000ms）**，避免多个节点同时超时反复触发选举；
  超时长度已保证一轮 `RequestVote` 往返足够（之前 150–300ms 太短会导致 term 狂涨、永远攒不够多数票）。

## 测试与验证（已实测通过）

- 构建 **3 节点集群**，真实编译运行（MSYS2 MinGW g++ 16.2.0）；
- **选举**：约 2 秒内选出唯一 Leader（`test_cluster.sh`）；
- **日志复制 / KV**：Leader `set foo bar` 后三节点日志均出现 `APPLY set foo = bar`；
- **故障转移**：kill 当前 Leader 后，剩余节点重新选举出新 Leader（`test_kv.sh` / `test_failover.sh`）；
- **持久化**：`raft_<id>.json` 落盘（term、votedFor、logs），重启可恢复。

> 说明：`get_kv` 目前是**本地读**（直接读本节点状态机，未做读仲裁），因此是**最终一致**而非严格的线性一致；
> 写请求只在 Leader 上受理（Follower 收到 `set` 返回 "not leader"，不自动转发）。

## 运行

> 依赖：C++17 编译器 + standalone Asio + nlohmann-json（CMake 自动拉取后两者）。
> 本仓库已在 MSYS2 MinGW g++ 16.2.0 上编译链接通过。

```bash
cmake -B build && cmake --build build

# 启动 3 节点集群（--id= 形式 + --peers 需含自己地址并按 id 索引）
./build/raft_node.exe --id=0 --peers=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102 &
./build/raft_node.exe --id=1 --peers=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102 &
./build/raft_node.exe --id=2 --peers=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102 &

# 交互命令（在某个节点进程的 stdin）
set foo bar      # 写 KV（需在 Leader 上）
get foo          # 读 KV（任意节点）
status           # 查节点角色/任期/Leader/日志长度
quit             # 退出
```

## 目录

```
Raft分布式共识引擎/
├── README.md
├── CMakeLists.txt
├── include/raft.h         # RaftNode 类声明 + RPC/日志/持久化结构
├── src/raft.cpp           # RPC 网络层 + RaftNodeWithRPC（KV 状态机）+ main
├── src/raft_node.cpp      # RaftNode 基类实现（选举 / 日志复制 / 持久化 / 定时器）
├── test_cluster.sh        # 3 节点选举测试
├── test_kv.sh             # 选举 + 故障转移测试（日志验证）
├── test_failover.sh       # Leader 故障转移测试
└── start_cluster.bat      # Windows 启动脚本
```

## 完成度

- **已实现**：领导人选举（随机超时 + RequestVote + 选举限制）、日志复制（AppendEntries + 冲突回退）、
  推进 commitIndex（只提交当前 term 条目）、持久化（term/votedFor/logs 落盘）、KV 状态机
  （apply_command set/del）、交互式命令行、心跳与复制定时器、故障转移。
- **已修 bug**：投票计数（`votes` 局部变量 → 成员）、序列化（nlohmann `adl_serializer`）、
  更高 term 响应未降级（旧 Leader 不退位）、退出时 io_thread 未 join 导致的 `std::terminate`、
  选举超时过短导致的 term 通胀、`status()` 输出的 JSON 引号。

## 已知限制 / TODO

- **无快照**：日志无限增长，不压缩（教学项目可接受）；
- **读不线性一致**：`get_kv` 本地直读，未实现 read-index / lease / 读仲裁；
- **写不转发**：Follower 收到 `set` 直接拒绝，不转发给 Leader；
- **无 CheckQuorum**：失去多数派的 Leader 不会主动下台（配合更高 term 响应降级，已缓解但未严格实现）；
- **RPC 无响应超时**：`pending_callbacks_` 在极端情况（对端永久不回包）可能累积；
- **持久化无 fsync**：`persist()` 未 fsync，崩溃时存在小窗口丢失；
- **`src/raft.cpp` 实为"头文件 + main"混合**：含 `#pragma once`，建议后续拆分为 `rpc_impl.h` + `main.cpp`（纯风格，不影响编译）。
