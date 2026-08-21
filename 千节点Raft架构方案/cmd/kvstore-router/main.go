// cmd/kvstore-router/main.go
//
// 路由层进程（无状态网关），将请求按 key 路由到对应分片 Leader。
package main

import (
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/distributed-kv/kvstore/pkg/metadata"
	"github.com/distributed-kv/kvstore/pkg/router"
)

func main() {
	endpoints := getEnv("METADATA_ENDPOINTS", "localhost:2379")
	meta, err := metadata.NewClusterTopology(strings.Split(endpoints, ","))
	if err != nil {
		log.Fatalf("failed to connect metadata: %v", err)
	}

	r := router.NewRouter(meta)
	addr := getEnv("LISTEN_ADDR", ":8080")

	log.Printf("router listening on %s (metadata: %s)", addr, endpoints)
	srv := r.NewHTTPServer(addr)
	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("router server error: %v", err)
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
