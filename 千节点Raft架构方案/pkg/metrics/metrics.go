// pkg/metrics/metrics.go
package metrics

import (
	"strconv"
	"sync/atomic"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	// 操作计数器
	operationsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "kv_operations_total",
			Help: "Total number of operations",
		},
		[]string{"operation", "shard", "status"},
	)

	// 操作延迟
	operationDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "kv_operation_duration_seconds",
			Help:    "Duration of operations",
			Buckets: []float64{.001, .005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
		},
		[]string{"operation", "shard"},
	)

	// Raft状态
	raftState = promauto.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "kv_raft_state",
			Help: "Raft state (0=follower, 1=candidate, 2=leader)",
		},
		[]string{"node", "shard"},
	)
)

// MetricsCollector 指标采集器
type MetricsCollector struct {
	nodeID  string
	shardID int
	ops     uint64
}

// NewMetricsCollector 创建指标采集器
func NewMetricsCollector(nodeID string) *MetricsCollector {
	return &MetricsCollector{
		nodeID: nodeID,
	}
}

// SetShardID 设置分片ID（用于指标标签）
func (m *MetricsCollector) SetShardID(shardID int) {
	m.shardID = shardID
}

// RecordOperation 记录操作计数
func (m *MetricsCollector) RecordOperation(op string, count int64) {
	atomic.AddUint64(&m.ops, uint64(count))
	operationsTotal.WithLabelValues(op, strconv.Itoa(m.shardID), "ok").Add(float64(count))
}

// RecordLatency 记录操作延迟
func (m *MetricsCollector) RecordLatency(op string, duration time.Duration) {
	operationDuration.WithLabelValues(op, strconv.Itoa(m.shardID)).Observe(duration.Seconds())
}

// SetRaftState 记录Raft状态
func (m *MetricsCollector) SetRaftState(state int) {
	raftState.WithLabelValues(m.nodeID, strconv.Itoa(m.shardID)).Set(float64(state))
}

// Ops 返回累计操作数
func (m *MetricsCollector) Ops() uint64 {
	return atomic.LoadUint64(&m.ops)
}
