# Makefile
.PHONY: all build build-node build-router build-client test bench clean docker-node docker-router

all: build

# 编译全部二进制
build: build-node build-router build-client
	go build ./...

# 编译数据节点
build-node:
	go build -o bin/kvstore-node ./cmd/kvstore-node

# 编译路由层
build-router:
	go build -o bin/kvstore-router ./cmd/kvstore-router

# 编译客户端 CLI
build-client:
	go build -o bin/kvstore-client ./cmd/kvstore-client

# 单元测试
test:
	go test ./...

# 数据节点镜像
docker-node:
	docker build -f Dockerfile.node -t kvstore-node:latest .

# 路由层镜像
docker-router:
	docker build -f Dockerfile.router -t kvstore-router:latest .

# 启动测试集群 (2分片 x 5节点)
cluster-test:
	bash scripts/start-cluster.sh --test

# 冒烟测试
smoke:
	bash scripts/test-cluster.sh

# 性能测试
bench:
	bash scripts/benchmark.sh --concurrency 100 --ops 10000

# 清理
clean:
	rm -rf bin
