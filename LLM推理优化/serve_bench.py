"""
serve_bench.py
==============

并发/批量 serving 吞吐与延迟基准 —— 推理优化 Step 4。

度量
----
- 不同 batch 大小下 serve N 个请求的**吞吐**（tokens/s）；
- 每请求延迟的 **P50 / P99**；
- 吞吐-延迟权衡曲线。

用法
----
.. code-block:: bash

    python 大模型/llm/serve_bench.py --train_steps 300
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import torch

# 让脚本可直接运行：把 大模型/ 加入模块搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gpt import GPT
from serving import batched_generate
from train_utils import encode, train_char_gpt

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
DATA_FILE = Path(__file__).resolve().parent.parent / "training_data.txt"

plt.switch_backend("Agg")  # 无显示环境下绘图


def serve_batch(model: GPT, prompts: torch.Tensor, batch_size: int, gen_len: int):
    """把 N 个请求按 batch_size 分批，返回 (总耗时 s, 每请求延迟列表 s)。"""
    latencies = []
    t0 = time.perf_counter()
    for i in range(0, prompts.size(0), batch_size):
        chunk = prompts[i : i + batch_size]
        t1 = time.perf_counter()
        batched_generate(model, chunk, gen_len=gen_len, sample=False)
        dt = time.perf_counter() - t1
        latencies.extend([dt] * chunk.size(0))
    total = time.perf_counter() - t0
    return total, latencies


def percentile(vals, p):
    if not vals:
        return 0.0
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(p * len(s))))
    return s[k]


def main() -> None:
    parser = argparse.ArgumentParser(description="并发 serving 基准")
    parser.add_argument("--train_steps", type=int, default=300)
    parser.add_argument("--train_kb", type=int, default=50)
    parser.add_argument("--n_requests", type=int, default=64)
    parser.add_argument("--prompt_len", type=int, default=16)
    parser.add_argument("--gen_len", type=int, default=32)
    parser.add_argument("--batch_sizes", type=str, default="1,4,8,16")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    batch_sizes = [int(x) for x in args.batch_sizes.split(",")]

    text = DATA_FILE.read_text(encoding="utf-8", errors="ignore")
    train_text = text[: args.train_kb * 1024]
    eval_text = text[args.train_kb * 1024 : (args.train_kb + 20) * 1024]

    print("训练模型 ...")
    model, char_to_idx, _ = train_char_gpt(
        train_text, n_layer=2, n_embd=64, n_head=2, steps=args.train_steps, seq_len=128
    )

    # 构造 N 个请求（不同位置切分，模拟不同请求）
    ids = encode(eval_text, char_to_idx)
    prompts = []
    step = max(1, len(ids) - args.prompt_len) // args.n_requests
    for i in range(args.n_requests):
        start = i * step
        prompts.append(torch.tensor(ids[start : start + args.prompt_len], dtype=torch.long))
    prompts = torch.stack(prompts)

    print("测量各 batch 大小 ...")
    results = {}
    for bs in batch_sizes:
        tps_list, p99_list, p50_list = [], [], []
        for _ in range(args.trials):
            total, lats = serve_batch(model, prompts, bs, args.gen_len)
            n_tok = args.n_requests * args.gen_len
            tps_list.append(n_tok / total)
            p99_list.append(percentile(lats, 0.99))
            p50_list.append(percentile(lats, 0.50))
        results[bs] = {
            "tps": sum(tps_list) / args.trials,
            "p50": sum(p50_list) / args.trials,
            "p99": sum(p99_list) / args.trials,
        }
        r = results[bs]
        print(
            f"  batch={bs:2d}: {r['tps']:.1f} tokens/s | p50 {r['p50'] * 1e3:.1f}ms | p99 {r['p99'] * 1e3:.1f}ms"
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 图 1：吞吐 vs batch size
    plt.figure(figsize=(8, 5))
    bs = list(results.keys())
    plt.plot(bs, [results[b]["tps"] for b in bs], marker="o", color="#2980b9")
    plt.xlabel("batch size")
    plt.ylabel("throughput (tokens/s)")
    plt.title("Throughput vs batch size")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    chart1 = REPORTS_DIR / "serving_throughput.png"
    plt.savefig(chart1, dpi=120)
    plt.close()

    # 图 2：延迟 vs batch size（P99）
    plt.figure(figsize=(8, 5))
    plt.plot(bs, [results[b]["p99"] * 1e3 for b in bs], marker="s", color="#e67e22")
    plt.xlabel("batch size")
    plt.ylabel("P99 latency (ms)")
    plt.title("P99 latency vs batch size")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    chart2 = REPORTS_DIR / "serving_latency.png"
    plt.savefig(chart2, dpi=120)
    plt.close()

    rows = "".join(
        f"| {b} | {results[b]['tps']:.1f} | {results[b]['p50'] * 1e3:.1f} | {results[b]['p99'] * 1e3:.1f} |\n"
        for b in bs
    )
    report = (
        f"# 并发/批量 serving 基准\n\n"
        f"- 模型参数：`{model.num_params():,}`；请求数 `{args.n_requests}`，"
        f"prompt `{args.prompt_len}`，生成 `{args.gen_len}`，`{args.trials}` 轮平均\n\n"
        f"| batch size | 吞吐 (tokens/s) | P50 (ms) | P99 (ms) |\n"
        f"|-----------|-----------------|----------|----------|\n{rows}\n"
        f"## 结论\n"
        f"- 增大 batch 显著提升吞吐（摊销单步前向固定开销）；\n"
        f"- 代价是单请求延迟上升（吞吐-延迟权衡）——这正是 serving 系统要平衡的指标；\n"
        f"- 真实系统（vLLM/TGI）在此基础上做 **continuous batching** 与 `PagedAttention`"
        f" 以进一步压延迟、提利用率。\n"
    )
    md = REPORTS_DIR / "serving_report.md"
    md.write_text(report, encoding="utf-8")

    print(f"\n报告: {md}\n图表: {chart1}, {chart2}")


if __name__ == "__main__":
    main()
