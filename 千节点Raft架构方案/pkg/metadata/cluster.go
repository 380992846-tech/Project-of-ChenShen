// pkg/metadata/cluster.go
package metadata

import (
	"context"
	"encoding/json"
	"fmt"
	"sort"
	"sync"
	"time"

	clientv3 "go.etcd.io/etcd/client/v3"
	"go.etcd.io/etcd/client/v3/concurrency"
)

// ClusterTopology 集群拓扑
type ClusterTopology struct {
	mu           sync.RWMutex
	etcdClient   *clientv3.Client
	shards       map[int]*ShardInfo
	nodeShardMap map[string]int // nodeID -> shardID
	version      int64
	listeners    []func(*ShardInfo)
}

type ShardInfo struct {
	ID       int      `json:"id"`
	Nodes    []string `json:"nodes"`
	Leader   string   `json:"leader"`
	StartKey string   `json:"start_key"`
	EndKey   string   `json:"end_key"`
	Status   string   `json:"status"` // active, migrating, readonly
	Term     uint64   `json:"term"`
}

type NodeInfo struct {
	ID       string    `json:"id"`
	Address  string    `json:"address"`
	ShardID  int       `json:"shard_id"`
	Status   string    `json:"status"` // online, offline, joining
	LastSeen time.Time `json:"last_seen"`
}

// NewClusterTopology 创建集群拓扑管理
func NewClusterTopology(endpoints []string) (*ClusterTopology, error) {
	client, err := clientv3.New(clientv3.Config{
		Endpoints:   endpoints,
		DialTimeout: 5 * time.Second,
	})
	if err != nil {
		return nil, err
	}

	ct := &ClusterTopology{
		etcdClient:   client,
		shards:       make(map[int]*ShardInfo),
		nodeShardMap: make(map[string]int),
	}

	if err := ct.loadTopology(); err != nil {
		return nil, err
	}

	go ct.watchTopology()
	return ct, nil
}

// loadTopology 从etcd加载拓扑
func (ct *ClusterTopology) loadTopology() error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	resp, err := ct.etcdClient.Get(ctx, "/topology/shards/", clientv3.WithPrefix())
	if err != nil {
		return err
	}

	ct.mu.Lock()
	defer ct.mu.Unlock()

	for _, kv := range resp.Kvs {
		var shard ShardInfo
		if err := json.Unmarshal(kv.Value, &shard); err != nil {
			continue
		}
		ct.shards[shard.ID] = &shard
		for _, node := range shard.Nodes {
			ct.nodeShardMap[node] = shard.ID
		}
	}
	return nil
}

// watchTopology 监听拓扑变化
func (ct *ClusterTopology) watchTopology() {
	watchChan := ct.etcdClient.Watch(context.Background(), "/topology/shards/", clientv3.WithPrefix())
	for resp := range watchChan {
		for _, ev := range resp.Events {
			var shard ShardInfo
			if err := json.Unmarshal(ev.Kv.Value, &shard); err != nil {
				continue
			}

			ct.mu.Lock()
			ct.shards[shard.ID] = &shard
			ct.version++
			listeners := append([]func(*ShardInfo){}, ct.listeners...)
			ct.mu.Unlock()

			// 通知所有监听者
			for _, fn := range listeners {
				fn(&shard)
			}
		}
	}
}

// OnShardChange 注册分片变化监听器
func (ct *ClusterTopology) OnShardChange(fn func(*ShardInfo)) {
	ct.mu.Lock()
	defer ct.mu.Unlock()
	ct.listeners = append(ct.listeners, fn)
}

// notifyShardChange 通知分片变化（兼容保留）
func (ct *ClusterTopology) notifyShardChange(shard *ShardInfo) {
	ct.mu.RLock()
	listeners := append([]func(*ShardInfo){}, ct.listeners...)
	ct.mu.RUnlock()
	for _, fn := range listeners {
		fn(shard)
	}
}

// GetShardForKey 根据key获取分片
func (ct *ClusterTopology) GetShardForKey(key string) *ShardInfo {
	ct.mu.RLock()
	defer ct.mu.RUnlock()

	// 按 StartKey 排序后二分查找
	keys := make([]int, 0, len(ct.shards))
	for id := range ct.shards {
		keys = append(keys, id)
	}
	sort.Ints(keys)

	for _, id := range keys {
		shard := ct.shards[id]
		if key >= shard.StartKey && (key < shard.EndKey || shard.EndKey == "") {
			return shard
		}
	}
	return nil
}

// GetShardNodes 获取分片的所有节点
func (ct *ClusterTopology) GetShardNodes(shardID int) []string {
	ct.mu.RLock()
	defer ct.mu.RUnlock()

	if shard, ok := ct.shards[shardID]; ok {
		return shard.Nodes
	}
	return nil
}

// UpdateLeader 更新分片Leader
func (ct *ClusterTopology) UpdateLeader(shardID int, leader string) error {
	ct.mu.Lock()
	defer ct.mu.Unlock()

	shard, ok := ct.shards[shardID]
	if !ok {
		return fmt.Errorf("shard %d not found", shardID)
	}

	shard.Leader = leader
	shard.Term++

	data, err := json.Marshal(shard)
	if err != nil {
		return err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	_, err = ct.etcdClient.Put(ctx, fmt.Sprintf("/topology/shards/%d", shardID), string(data))
	return err
}

// RegisterShard 注册或更新分片（使用 etcd 事务防止并发写冲突）
func (ct *ClusterTopology) RegisterShard(shard *ShardInfo) error {
	data, err := json.Marshal(shard)
	if err != nil {
		return err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	key := fmt.Sprintf("/topology/shards/%d", shard.ID)
	s, err := concurrency.NewSession(ct.etcdClient)
	if err != nil {
		return err
	}
	defer s.Close()

	_, err = ct.etcdClient.Put(ctx, key, string(data))
	return err
}

// Close 关闭 etcd 连接
func (ct *ClusterTopology) Close() error {
	return ct.etcdClient.Close()
}
