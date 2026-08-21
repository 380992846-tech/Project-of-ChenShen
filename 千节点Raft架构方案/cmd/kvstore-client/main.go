// cmd/kvstore-client/main.go
//
// 客户端 CLI，通过 SDK 对集群进行读写。
// 用法：
//
//	kvstore-client set <key> <value>
//	kvstore-client get <key>
//	kvstore-client del <key>
package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"strings"

	"github.com/distributed-kv/kvstore/pkg/client"
)

func main() {
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: kvstore-client [--metadata e1,e2,...] <set|get|del> <key> [value]\n")
	}
	metadataEP := flag.String("metadata", "http://localhost:2379", "etcd 端点(逗号分隔)")
	flag.Parse()

	args := flag.Args()
	if len(args) < 2 {
		flag.Usage()
		os.Exit(1)
	}

	op := args[0]
	key := args[1]

	c, err := client.NewClient(strings.Split(*metadataEP, ","))
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to create client: %v\n", err)
		os.Exit(1)
	}
	defer c.Close()

	ctx := context.Background()

	switch op {
	case "set":
		if len(args) < 3 {
			fmt.Fprintln(os.Stderr, "set 需要 value 参数")
			os.Exit(1)
		}
		if err := c.Set(ctx, key, args[2]); err != nil {
			fmt.Fprintf(os.Stderr, "set failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("ok")
	case "get":
		val, err := c.Get(ctx, key)
		if err != nil {
			fmt.Fprintf(os.Stderr, "get failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println(val)
	case "del":
		if err := c.Delete(ctx, key); err != nil {
			fmt.Fprintf(os.Stderr, "del failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("ok")
	default:
		fmt.Fprintf(os.Stderr, "unknown op: %s\n", op)
		os.Exit(1)
	}
}
