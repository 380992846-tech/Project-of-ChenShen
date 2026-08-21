// pkg/router/router.go
package router

import (
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/gorilla/mux"
	"go.uber.org/zap"

	"github.com/distributed-kv/kvstore/pkg/metadata"
)

// Router 路由层
type Router struct {
	mu           sync.RWMutex
	metadata     *metadata.ClusterTopology
	shardClients map[int]*ShardClient
	logger       *zap.Logger
	httpServer   *http.Server
	requestCount int64
}

// ShardClient 分片客户端
type ShardClient struct {
	shardID    int
	leaderAddr string
	nodes      []string
	lastUpdate time.Time
	httpClient *http.Client
}

// NewRouter 创建路由器
func NewRouter(metadata *metadata.ClusterTopology) *Router {
	router := &Router{
		metadata:     metadata,
		shardClients: make(map[int]*ShardClient),
		logger:       zap.L(),
	}

	router.initShardClients()
	return router
}

// initShardClients 初始化所有分片客户端
func (r *Router) initShardClients() {
	// 获取所有分片
	// 为每个分片创建客户端
	// 此处实际应遍历 metadata 中所有分片，这里保留骨架
}

// Route 路由请求
func (r *Router) Route(key string) (*ShardClient, error) {
	// 1. 从元数据获取分片
	shard := r.metadata.GetShardForKey(key)
	if shard == nil {
		return nil, fmt.Errorf("no shard for key: %s", key)
	}

	// 2. 获取或创建分片客户端
	r.mu.RLock()
	client, ok := r.shardClients[shard.ID]
	r.mu.RUnlock()

	if !ok || client.leaderAddr != shard.Leader {
		// 创建新客户端
		client = r.createShardClient(shard)
		r.mu.Lock()
		r.shardClients[shard.ID] = client
		r.mu.Unlock()
	}

	return client, nil
}

// createShardClient 创建分片客户端
func (r *Router) createShardClient(shard *metadata.ShardInfo) *ShardClient {
	return &ShardClient{
		shardID:    shard.ID,
		leaderAddr: shard.Leader,
		nodes:      shard.Nodes,
		lastUpdate: time.Now(),
		httpClient: &http.Client{
			Timeout: 5 * time.Second,
		},
	}
}

// HandleRequest 处理请求
func (r *Router) HandleRequest(w http.ResponseWriter, req *http.Request) {
	vars := mux.Vars(req)
	key := vars["key"]

	// 路由到对应分片
	client, err := r.Route(key)
	if err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}

	// 转发到Leader
	// 实际实现中，这里需要转发请求
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(fmt.Sprintf("Routed to shard %d leader %s", client.shardID, client.leaderAddr)))
}

// NewHTTPServer 创建HTTP路由服务
func (r *Router) NewHTTPServer(addr string) *http.Server {
	muxRouter := mux.NewRouter()
	muxRouter.HandleFunc("/api/v1/key/{key}", r.HandleRequest).Methods(http.MethodGet, http.MethodPut, http.MethodDelete)

	r.httpServer = &http.Server{
		Addr:         addr,
		Handler:      muxRouter,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}
	return r.httpServer
}
