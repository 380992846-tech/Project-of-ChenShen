// cmd/kvstore-node/main.go
//
// kvstore-node 数据节点进程。
// 用法示例：
//
//	./kvstore-node \
//	    --node-id node-0-0 \
//	    --shard-id 0 \
//	    --bind-addr 127.0.0.1:8000 \
//	    --raft-dir /tmp/raft/node-0-0 \
//	    --metadata http://localhost:2370,http://localhost:2371,...
//	    --bootstrap
package main

import (
	"flag"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/prometheus/client_golang/prometheus/promhttp"

	"github.com/distributed-kv/kvstore/pkg/metadata"
	"github.com/distributed-kv/kvstore/pkg/raft"
)

func main() {
	var (
		nodeID     = flag.String("node-id", "", "当前节点 ID")
		shardID    = flag.Int("shard-id", 0, "所属分片 ID")
		bindAddr   = flag.String("bind-addr", "", "Raft 监听地址")
		raftDir    = flag.String("raft-dir", "", "Raft 数据目录")
		metadataEP = flag.String("metadata", "", "etcd 元数据集群端点(逗号分隔)")
		bootstrap  = flag.Bool("bootstrap", false, "作为分片第一个节点初始化集群")
		httpAddr   = flag.String("http-addr", "", "HTTP API 监听地址(可选)")
		metricsEP  = flag.String("metrics-addr", ":9100", "Prometheus metrics 监听地址")
	)
	flag.Parse()

	if *nodeID == "" || *bindAddr == "" || *raftDir == "" {
		log.Fatal("--node-id, --bind-addr, --raft-dir 为必填参数")
	}

	// 1. 启动 Raft KV 节点
	store, err := raft.NewKVStore(*nodeID, *shardID, *bindAddr, *raftDir)
	if err != nil {
		log.Fatalf("failed to create kv store: %v", err)
	}

	if *bootstrap {
		if err := store.Bootstrap(); err != nil {
			log.Fatalf("failed to bootstrap cluster: %v", err)
		}
		log.Printf("node %s bootstrapped shard %d", *nodeID, *shardID)
	} else {
		if err := store.Join(); err != nil {
			log.Printf("join may be no-op (already joined): %v", err)
		}
	}

	// 2. 上报拓扑到元数据集群
	// 实际生产实现中，应在此将本节点及其分片信息注册到 etcd：
	//   shardInfo := &metadata.ShardInfo{ID: *shardID, Nodes: []string{*nodeID}, ...}
	//   ct.RegisterShard(shardInfo)
	_ = metadataEP
	_ = metadata.NewClusterTopology

	// 3. 暴露 metrics
	go func() {
		http.Handle("/metrics", promhttp.Handler())
		log.Printf("metrics listening on %s", *metricsEP)
		if err := http.ListenAndServe(*metricsEP, nil); err != nil {
			log.Printf("metrics server error: %v", err)
		}
	}()

	// 4. 等待退出信号
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	<-ch

	log.Printf("node %s shutting down", *nodeID)
	if err := store.Shutdown(); err != nil {
		log.Printf("shutdown error: %v", err)
	}
}
