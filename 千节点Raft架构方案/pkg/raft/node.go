// pkg/raft/node.go
package raft

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/hashicorp/raft"
	raftboltdb "github.com/hashicorp/raft-boltdb/v2"

	"github.com/distributed-kv/kvstore/pkg/metrics"
)

// KVStore 键值存储 - 每个Raft节点
type KVStore struct {
	mu       sync.RWMutex
	raft     *raft.Raft
	store    map[string]string
	fsm      *FSM
	nodeID   string
	shardID  int
	raftDir  string
	bindAddr string
	metrics  *metrics.MetricsCollector
}

// FSM 状态机
type FSM struct {
	mu    sync.RWMutex
	store map[string]string
}

type Command struct {
	Op    string `json:"op"` // set, delete
	Key   string `json:"key"`
	Value string `json:"value"`
}

// NewKVStore 创建KV存储节点
func NewKVStore(nodeID string, shardID int, bindAddr string, raftDir string) (*KVStore, error) {
	store := &KVStore{
		nodeID:   nodeID,
		shardID:  shardID,
		store:    make(map[string]string),
		raftDir:  raftDir,
		bindAddr: bindAddr,
		fsm: &FSM{
			store: make(map[string]string),
		},
		metrics: metrics.NewMetricsCollector(nodeID),
	}

	if err := os.MkdirAll(raftDir, 0o755); err != nil {
		return nil, err
	}

	if err := store.setupRaft(); err != nil {
		return nil, err
	}

	return store, nil
}

// setupRaft 配置Raft
func (ks *KVStore) setupRaft() error {
	config := raft.DefaultConfig()
	config.LocalID = raft.ServerID(ks.nodeID)
	config.HeartbeatTimeout = 100 * time.Millisecond
	config.ElectionTimeout = 1 * time.Second
	config.LeaderLeaseTimeout = 500 * time.Millisecond
	config.SnapshotInterval = 60 * time.Second
	config.SnapshotThreshold = 1000
	config.MaxAppendEntries = 64

	// 日志存储
	logStore, err := raftboltdb.NewBoltStore(filepath.Join(ks.raftDir, "raft-log.db"))
	if err != nil {
		return err
	}

	// 稳定存储
	stableStore, err := raftboltdb.NewBoltStore(filepath.Join(ks.raftDir, "raft-stable.db"))
	if err != nil {
		return err
	}

	// 快照存储
	snapshotStore, err := raft.NewFileSnapshotStore(filepath.Join(ks.raftDir, "snapshots"), 3, os.Stderr)
	if err != nil {
		return err
	}

	// 传输层
	addr, err := net.ResolveTCPAddr("tcp", ks.bindAddr)
	if err != nil {
		return err
	}
	transport, err := raft.NewTCPTransport(ks.bindAddr, addr, 3, 10*time.Second, os.Stderr)
	if err != nil {
		return err
	}

	// 创建Raft实例
	raf, err := raft.NewRaft(config, ks.fsm, logStore, stableStore, snapshotStore, transport)
	if err != nil {
		return err
	}

	ks.raft = raf
	return nil
}

// Bootstrap 作为第一个节点初始化集群
func (ks *KVStore) Bootstrap() error {
	if ks.raft.State() != raft.Follower && ks.raft.State() != raft.Candidate {
		return nil
	}
	configuration := raft.Configuration{
		Servers: []raft.Server{
			{
				ID:      raft.ServerID(ks.nodeID),
				Address: raft.ServerAddress(ks.bindAddr),
			},
		},
	}
	future := ks.raft.BootstrapCluster(configuration)
	return future.Error()
}

// Join 加入Raft集群
func (ks *KVStore) Join() error {
	future := ks.raft.AddVoter(raft.ServerID(ks.nodeID), raft.ServerAddress(ks.bindAddr), 0, 0)
	return future.Error()
}

// IsLeader 判断是否为Leader
func (ks *KVStore) IsLeader() bool {
	return ks.raft.State() == raft.Leader
}

// GetLeader 获取当前Leader
func (ks *KVStore) GetLeader() (string, bool) {
	return string(ks.raft.Leader()), ks.raft.Leader() != ""
}

// Set 设置键值
func (ks *KVStore) Set(key, value string) error {
	if ks.raft.State() != raft.Leader {
		return fmt.Errorf("not leader")
	}

	cmd := Command{
		Op:    "set",
		Key:   key,
		Value: value,
	}

	data, err := encodeCommand(cmd)
	if err != nil {
		return err
	}

	start := time.Now()
	future := ks.raft.Apply(data, 5*time.Second)
	if err := future.Error(); err != nil {
		return err
	}

	resp := future.Response()
	if resp != nil {
		if err, ok := resp.(error); ok {
			return err
		}
	}

	ks.metrics.RecordOperation("set", 1)
	ks.metrics.RecordLatency("set", time.Since(start))
	return nil
}

// Delete 删除键值
func (ks *KVStore) Delete(key string) error {
	if ks.raft.State() != raft.Leader {
		return fmt.Errorf("not leader")
	}

	cmd := Command{
		Op:  "delete",
		Key: key,
	}

	data, err := encodeCommand(cmd)
	if err != nil {
		return err
	}

	start := time.Now()
	future := ks.raft.Apply(data, 5*time.Second)
	if err := future.Error(); err != nil {
		return err
	}

	ks.metrics.RecordOperation("delete", 1)
	ks.metrics.RecordLatency("delete", time.Since(start))
	return nil
}

// Get 获取键值
func (ks *KVStore) Get(key string) (string, bool) {
	ks.mu.RLock()
	defer ks.mu.RUnlock()

	val, ok := ks.fsm.store[key]
	return val, ok
}

// State 返回Raft状态
func (ks *KVStore) State() raft.RaftState {
	return ks.raft.State()
}

// Stats 返回Raft统计信息
func (ks *KVStore) Stats() map[string]string {
	return ks.raft.Stats()
}

// Shutdown 关闭节点
func (ks *KVStore) Shutdown() error {
	future := ks.raft.Shutdown()
	return future.Error()
}

// encodeCommand 编码命令
func encodeCommand(cmd Command) ([]byte, error) {
	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	if err := enc.Encode(cmd); err != nil {
		return nil, err
	}
	return buf.Bytes(), nil
}

// FSM Apply 实现
func (fsm *FSM) Apply(log *raft.Log) interface{} {
	var cmd Command
	buf := bytes.NewReader(log.Data)
	dec := gob.NewDecoder(buf)
	if err := dec.Decode(&cmd); err != nil {
		return err
	}

	fsm.mu.Lock()
	defer fsm.mu.Unlock()

	switch cmd.Op {
	case "set":
		fsm.store[cmd.Key] = cmd.Value
	case "delete":
		delete(fsm.store, cmd.Key)
	}

	return nil
}

// Snapshot 实现
func (fsm *FSM) Snapshot() (raft.FSMSnapshot, error) {
	fsm.mu.RLock()
	defer fsm.mu.RUnlock()

	// 复制数据
	storeCopy := make(map[string]string)
	for k, v := range fsm.store {
		storeCopy[k] = v
	}

	return &Snapshot{store: storeCopy}, nil
}

// Restore 实现
func (fsm *FSM) Restore(snapshot io.ReadCloser) error {
	defer snapshot.Close()

	dec := gob.NewDecoder(snapshot)
	var store map[string]string
	if err := dec.Decode(&store); err != nil {
		return err
	}

	fsm.mu.Lock()
	defer fsm.mu.Unlock()
	fsm.store = store
	return nil
}

// Snapshot 快照结构
type Snapshot struct {
	store map[string]string
}

func (s *Snapshot) Persist(sink raft.SnapshotSink) error {
	enc := gob.NewEncoder(sink)
	if err := enc.Encode(s.store); err != nil {
		sink.Cancel()
		return err
	}
	return sink.Close()
}

func (s *Snapshot) Release() {}
