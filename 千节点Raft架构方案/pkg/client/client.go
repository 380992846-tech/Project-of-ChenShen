// pkg/client/client.go
package client

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"

	"github.com/distributed-kv/kvstore/pkg/metadata"
)

// Client SDK客户端
type Client struct {
	mu         sync.RWMutex
	metadata   *metadata.ClusterTopology
	httpClient *http.Client
	routeCache map[string]*RouteInfo
	endpoints  []string
}

type RouteInfo struct {
	ShardID    int
	LeaderAddr string
	ExpireAt   time.Time
	Nodes      []string
}

// NewClient 创建客户端
func NewClient(endpoints []string) (*Client, error) {
	metadataClient, err := metadata.NewClusterTopology(endpoints)
	if err != nil {
		return nil, err
	}

	return &Client{
		metadata:   metadataClient,
		httpClient: &http.Client{Timeout: 5 * time.Second},
		routeCache: make(map[string]*RouteInfo),
		endpoints:  endpoints,
	}, nil
}

// Get 获取值
func (c *Client) Get(ctx context.Context, key string) (string, error) {
	route, err := c.getRoute(key)
	if err != nil {
		return "", err
	}

	url := fmt.Sprintf("http://%s/api/v1/key/%s", route.LeaderAddr, key)
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return "", err
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		// 路由缓存失效，重新获取
		c.invalidateRoute(key)
		return c.Get(ctx, key)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("get failed: %s", resp.Status)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	var result struct {
		Value string `json:"value"`
	}
	if err := json.Unmarshal(body, &result); err != nil {
		return "", err
	}

	return result.Value, nil
}

// Set 设置值
func (c *Client) Set(ctx context.Context, key, value string) error {
	route, err := c.getRoute(key)
	if err != nil {
		return err
	}

	data := map[string]string{"key": key, "value": value}
	jsonData, _ := json.Marshal(data)

	url := fmt.Sprintf("http://%s/api/v1/key/%s", route.LeaderAddr, key)
	req, err := http.NewRequestWithContext(ctx, "PUT", url, bytes.NewReader(jsonData))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		c.invalidateRoute(key)
		return c.Set(ctx, key, value)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("set failed: %s", resp.Status)
	}

	return nil
}

// Delete 删除键值
func (c *Client) Delete(ctx context.Context, key string) error {
	route, err := c.getRoute(key)
	if err != nil {
		return err
	}

	url := fmt.Sprintf("http://%s/api/v1/key/%s", route.LeaderAddr, key)
	req, err := http.NewRequestWithContext(ctx, "DELETE", url, nil)
	if err != nil {
		return err
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		c.invalidateRoute(key)
		return c.Delete(ctx, key)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("delete failed: %s", resp.Status)
	}

	return nil
}

// getRoute 获取路由信息
func (c *Client) getRoute(key string) (*RouteInfo, error) {
	c.mu.RLock()
	route, ok := c.routeCache[key]
	c.mu.RUnlock()

	if ok && time.Now().Before(route.ExpireAt) {
		return route, nil
	}

	// 从元数据获取
	shard := c.metadata.GetShardForKey(key)
	if shard == nil {
		return nil, fmt.Errorf("key %s not found", key)
	}

	route = &RouteInfo{
		ShardID:    shard.ID,
		LeaderAddr: shard.Leader,
		ExpireAt:   time.Now().Add(10 * time.Second), // TTL 10秒
		Nodes:      shard.Nodes,
	}

	c.mu.Lock()
	c.routeCache[key] = route
	c.mu.Unlock()

	return route, nil
}

// invalidateRoute 使路由缓存失效
func (c *Client) invalidateRoute(key string) {
	c.mu.Lock()
	delete(c.routeCache, key)
	c.mu.Unlock()
}

// Close 关闭客户端
func (c *Client) Close() error {
	return c.metadata.Close()
}
