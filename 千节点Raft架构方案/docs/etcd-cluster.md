# etcd 元数据集群部署详解

本项目使用 etcd（v3.5）作为元数据集群，负责保存分片映射、节点状态与 Leader 信息。本文档详细说明 etcd 集群的启动参数、部署模式、以及与本项目的对接方式。

---

## 1. 为什么用 etcd 做元数据集群

- **内置 Raft 共识**：etcd 本身就是基于 Raft 的一致性 KV，天然具备高可用。
- **Watch 机制**：本项目通过 `clientv3.Watch` 监听 `/topology/shards/` 前缀，实现拓扑变化的实时同步。
- **事务与租约**：支持 `concurrency.Session` 节点心跳/租约、以及 Leader 更新的并发安全写入。
- **成熟稳定**：Kubernetes、TiKV（PD）等大量生产系统均以 etcd 作为元数据/协调存储。

---

## 2. 单节点快速启动（本地开发）

```bash
# 单节点，仅用于本地调试
etcd \
  --name local-etcd \
  --data-dir /tmp/etcd-local \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster local-etcd=http://0.0.0.0:2380 \
  --initial-cluster-token local-cluster \
  --initial-cluster-state new

# 验证
etcdctl --endpoints=http://localhost:2379 endpoint health
```

> 单节点仅用于验证，生产/测试集群必须 ≥ 3 节点（推荐 5 节点）。

---

## 3. 5 节点集群部署（与 start-cluster.sh 一致）

脚本 `scripts/start-cluster.sh` 使用以下参数启动 5 个 etcd 节点：

| 参数 | 作用 |
|------|------|
| `--name` | 节点名，集群内唯一 |
| `--data-dir` | 数据目录（WAL + 快照） |
| `--listen-client-urls` | 客户端（本项目 router/SDK/数据节点）连接地址 |
| `--advertise-client-urls` | 对外公告的客户端地址 |
| `--listen-peer-urls` | 节点间 Raft 通信监听地址 |
| `--initial-advertise-peer-urls` | 对外公告的 peer 地址 |
| `--initial-cluster` | 引导时整个集群的成员列表（`name=peer-url`） |
| `--initial-cluster-token` | 集群标识，避免误加错集群 |
| `--initial-cluster-state` | `new`（新建）或 `existing`（加入已有） |

**端口规划（本地脚本）**

| 节点 | client URL | peer URL |
|------|-----------|----------|
| metadata-0 | `http://localhost:2370` | `http://localhost:2380` |
| metadata-1 | `http://localhost:2371` | `http://localhost:2381` |
| metadata-2 | `http://localhost:2372` | `http://localhost:2382` |
| metadata-3 | `http://localhost:2373` | `http://localhost:2383` |
| metadata-4 | `http://localhost:2374` | `http://localhost:2384` |

**成员列表初始化**

```bash
INITIAL_CLUSTER="metadata-0=http://localhost:2380,metadata-1=http://localhost:2381,metadata-2=http://localhost:2382,metadata-3=http://localhost:2383,metadata-4=http://localhost:2384"

etcd --name metadata-0 --data-dir /tmp/etcd-0 \
     --listen-client-urls http://localhost:2370 \
     --advertise-client-urls http://localhost:2370 \
     --listen-peer-urls http://localhost:2380 \
     --initial-advertise-peer-urls http://localhost:2380 \
     --initial-cluster "$INITIAL_CLUSTER" \
     --initial-cluster-token kvstore-meta \
     --initial-cluster-state new
# ... 其余 4 个节点同理，替换 name/端口
```

> 关键点：**只有 `--initial-cluster-state=new` 的首个节点需要完整的 `--initial-cluster` 成员列表**；若集群已建立，后续节点应使用 `--initial-cluster-state=existing`，并通过 `etcdctl member add` 先加入。

---

## 4. 集群启动流程（生产建议）

```bash
# 4.1 首节点引导（一次性）
etcd --name meta-0 --initial-cluster-state new ... &

# 4.2 用 member add 动态加入其余节点
etcdctl member add meta-1 --peer-urls=http://meta-1:2380
etcdctl member add meta-2 --peer-urls=http://meta-2:2380
# ... 返回的 INITIAL_CLUSTER 字符串用于启动对应节点

# 4.3 验证集群成员与健康
etcdctl member list
etcdctl --endpoints=http://meta-0:2379,http://meta-1:2379 endpoint health
```

> **注意**：5 节点 etcd 集群最多容忍 **2 个节点故障**（`(5-1)/2 = 2`）。若同时故障 ≥3 个节点，将无法选举，元数据集群不可用。

---

## 5. Docker Compose 方式（生产推荐）

已在 `docker-compose.yml` 中定义 5 个 etcd 服务。启动方式：

```bash
# 启动全部服务（etcd×5 + 路由 + Prometheus + Grafana）
docker compose up -d metadata-0 metadata-1 metadata-2 metadata-3 metadata-4

# 验证
docker compose exec metadata-0 etcdctl --endpoints=http://localhost:2379 endpoint health
docker compose exec metadata-0 etcdctl member list
```

各节点在容器内的 client 端口统一为 `2379`，通过服务名互访：

```
metadata-0:2379, metadata-1:2379, metadata-2:2379, metadata-3:2379, metadata-4:2379
```

---

## 6. 本项目如何对接 etcd

本项目所有组件通过 etcd client 端点列表连接元数据集群：

### 数据节点（kvstore-node）

启动参数 `--metadata` 传入 etcd 端点，节点启动后注册自身分片信息：

```go
// 启动后注册自身（示意）
ct, _ := metadata.NewClusterTopology(endpoints)
ct.RegisterShard(&metadata.ShardInfo{
    ID:    shardID,
    Nodes: []string{nodeID},
    // Leader 由选举后更新
})
```

### 路由层（kvstore-router）

启动时通过 `METADATA_ENDPOINTS` 环境变量连接 etcd，查询分片映射：

```go
meta, _ := metadata.NewClusterTopology(strings.Split(endpoints, ","))
r := router.NewRouter(meta) // 内部调用 meta.GetShardForKey(key)
```

### 客户端 SDK

```go
c, _ := client.NewClient([]string{"http://localhost:2370", "..."})
// 内部维护 etcd 连接 + 路由缓存（TTL 10s）
```

---

## 7. 常用运维命令

```bash
# 健康检查
etcdctl --endpoints=http://meta-0:2379 endpoint health

# 成员管理
etcdctl member list
etcdctl member add <name> --peer-urls=<url>
etcdctl member remove <id>

# 查看本项目写入的拓扑数据
etcdctl --endpoints=http://localhost:2370 get /topology/shards/ --prefix
etcdctl --endpoints=http://localhost:2370 get /topology/shards/0

# 备份（定期执行）
etcdctl snapshot save /backup/etcd-$(date +%F).db

# 恢复
etcdctl snapshot restore /backup/etcd-xxx.db \
  --data-dir /tmp/etcd-restore \
  --initial-cluster meta-0=http://localhost:2380 \
  --initial-cluster-token kvstore-meta
```

---

## 8. 故障与排障

| 现象 | 可能原因 | 排查 |
|------|----------|------|
| 无法连接 etcd | 端口未开放 / 地址错误 | `etcdctl endpoint health`、检查防火墙 |
| 数据目录占用/锁 | 单节点同时被多个进程启动 | 停止后 `--data-dir` 重新初始化 |
| 集群选举失败 | 节点数不足 / 网络分区 | `etcdctl member list`、查看日志中 leader 选举 |
| `member add` 后不启动 | 缺少返回的 `INITIAL_CLUSTER` | 使用 `etcdctl member add` 输出的完整参数 |
| 客户端超时 | etcd 集群已不可用 | 检查成员健康、日志 `etcd --log-level=debug` |
