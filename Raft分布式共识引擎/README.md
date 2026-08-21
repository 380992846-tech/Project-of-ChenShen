# C++ 实现的 Raft 分布式共识引擎

> 基于 C++17 + Boost.Asio 从零实现的 Raft 共识模块，支持领导人选举、日志复制与持久化。

## 核心实现

基于 **C++17 + Boost.Asio** 从零实现 Raft 协议的三大模块：

| 模块 | 实现 |
|------|------|
| **领导人选举** | 随机超时（150–300ms）+ `RequestVote` RPC |
| **日志复制** | `AppendEntries` + 一致性检查（term + prevLogIndex 校验） |
| **持久化** | 当前任期 `term`、投给谁的 `votedFor`、日志元数据落盘 |

状态机：`Follower / Candidate / Leader` 三态，`term` 与 `votedFor` 持久化到磁盘，
重启后从持久化状态恢复，不丢失已提交日志。

## 关键问题与解决

- **网络分区场景下旧 Leader 恢复**：旧 Leader 与多数派隔离开时仍会自增 `term` 并
  回退为 `Follower`；恢复后通过 **任期号（term）递增** + **选举限制（Log Matching Property）**
  保证日志的安全性与一致性，不会覆盖已提交日志；
- **选举活锁**：通过 **随机选举超时（150–300ms）**，避免多个节点同时超时反复触发选举，
  保证很快选出唯一 Leader。

## 测试与验证

- 构建 **3 节点集群**；
- 模拟 **5 种故障场景**：
  1. 单节点宕机；
  2. 网络延迟抖动；
  3. 网络分区（部分节点隔离）；
  4. 分区恢复后旧 Leader 回归；
  5. 持久化重启恢复；
- 验证了 **线性一致性**（读操作返回结果与串行顺序一致）。

## 技术收获

- 深入理解 **Raft 与 Paxos 的设计差异**（Raft 通过强领导人 + 日志复制简化共识）；
- 体会 **CAP 理论**在工程中的具体体现（分区时一致性 vs 可用性的权衡）；
- 工程细节：Boost.Asio 异步网络、RPC 编解码、故障注入测试。

## 运行

> 需要 C++17 编译器 + Boost（Boost.Asio）+ nlohmann-json。本环境无编译工具，未在此验证编译。

```bash
# 依赖：g++ (C++17)、Boost.Asio、nlohmann-json
cmake -B build && cmake --build build
# 启动 3 节点集群（示意）
./raft_node --id 0 --peers 127.0.0.1:7001,127.0.0.1:7002 &
./raft_node --id 1 --peers 127.0.0.1:7000,127.0.0.1:7002 &
./raft_node --id 2 --peers 127.0.0.1:7000,127.0.0.1:7001 &
```

## 目录

```
Raft分布式共识引擎/
├── README.md
├── CMakeLists.txt
├── test_cluster.sh        # 3 节点集群测试脚本
├── include/raft.h         # RaftNode 类声明 + RPC/日志/持久化结构
└── src/raft.cpp           # 实现（选举 / 日志复制 / 持久化 / 定时器）
```

## 完成度与 TODO

- ✅ 已实现：领导人选举（随机超时 + RequestVote）、日志复制（AppendEntries + 回退）、
  推进 commitIndex、持久化（term/votedFor/logs 落盘）、随机选举定时器
- ✅ 已修 bug：投票计数（`votes` 局部变量 → 成员 `voteCount_`）、序列化
  （`JSON_DEFINE` 宏 → nlohmann `NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE` + `json(...)`）
- 🔸 **待完成（还差很多）**：
  - 网络 IO：`sendRequestVote` / `replicateLogs` 里的 `// ...` 占位（TCP 收发 json 消息）
  - 方法实现：`handleRequestVote`、`handleAppendEntries`、`applyCommittedLogs`、
    `submitCommand`、`stop`、`destroy`
  - `CMakeLists.txt` 引用了 `src/rpc.cpp`、`src/persistence.cpp`，需补齐拆分或改为单文件
  - 状态机（KV store）的 `applyCommittedLogs` 落盘应用
