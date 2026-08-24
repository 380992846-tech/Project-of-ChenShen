#!/usr/bin/env python3
"""A800 三位一体闭环采集：吞吐 / 延迟 / 功耗（perf-per-watt）。

前提：vLLM serve 已在某端口运行（OpenAI 兼容 ``/v1/completions``，默认 127.0.0.1:8000）。
并发压测统计**吞吐 + 请求总延迟(p50/p99)**，同时后台线程用 NVML 采**功耗**。

用法：
    python scripts/e2e_bench.py --concurrency 8 --requests 100 --max-tokens 128

说明
----
- 延迟为**每请求总时延**（含排队 + 生成），非流式 TTFT；如需 TTFT 请改走 streaming 并统计首 token。
- 功耗为压测期间 NVML 平均读数。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "software"))

import pynvml  # noqa: E402


def _nvml_handle():
    pynvml.nvmlInit()
    return pynvml.nvmlDeviceGetHandleByIndex(0), pynvml


def call_once(base: str, model: str, prompt: str, max_tokens: int) -> tuple[int, float]:
    body = json.dumps({"model": model, "prompt": prompt, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(base, data=body, headers={"Content-Type": "application/json"})
    t = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=180))
    return r["usage"]["completion_tokens"], time.time() - t


def main() -> int:
    ap = argparse.ArgumentParser(description="三位一体：吞吐/延迟/功耗")
    ap.add_argument("--url", default="http://127.0.0.1:8000/v1/completions")
    ap.add_argument("--model", default="Qwen/Qwen2-7B-Instruct")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--requests", type=int, default=100)
    ap.add_argument("--max-tokens", type=int, default=128)
    ap.add_argument("--prompt", default="清华园的二校门，古朴庄重，四季各有不同的风景。" * 6)
    args = ap.parse_args()

    powers: list[float] = []
    stop = threading.Event()

    def poll() -> None:
        try:
            handle, nvml = _nvml_handle()
            while not stop.is_set():
                powers.append(nvml.nvmlDeviceGetPowerUsage(handle) / 1000.0)
                time.sleep(0.5)
        except Exception:
            pass

    pt = threading.Thread(target=poll, daemon=True)
    pt.start()

    # 并发压测
    results: list[tuple[int, float]] = []
    lock = threading.Lock()

    def worker() -> None:
        for _ in range(max(1, args.requests // args.concurrency)):
            try:
                ct, dt = call_once(args.url, args.model, args.prompt, args.max_tokens)
                with lock:
                    results.append((ct, dt))
            except Exception:
                pass

    t0 = time.time()
    ths = [threading.Thread(target=worker) for _ in range(args.concurrency)]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    elapsed = time.time() - t0
    stop.set()
    pt.join(timeout=2)

    total_tok = sum(c for c, _ in results)
    lats = sorted(dt for _, dt in results)
    p50 = lats[len(lats) // 2] if lats else 0.0
    p99 = lats[int(len(lats) * 0.99)] if lats else 0.0
    avg_power = sum(powers) / len(powers) if powers else 0.0
    tps = total_tok / elapsed if elapsed > 0 else 0.0
    ppw = tps / avg_power if avg_power > 0 else 0.0

    print("=" * 56)
    print(f"吞吐 (tokens/s)   : {tps:.1f}")
    print(f"请求完成          : {len(results)} / {args.requests}")
    print(f"总 token          : {total_tok}")
    print(f"延迟 p50 / p99    : {p50 * 1e3:.0f} / {p99 * 1e3:.0f} ms")
    print(f"平均功耗          : {avg_power:.1f} W")
    print(f"perf-per-watt     : {ppw:.3f} tok/s/W")
    print("=" * 56)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
