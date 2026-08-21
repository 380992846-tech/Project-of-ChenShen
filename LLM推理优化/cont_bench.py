"""
cont_bench.py
=============

continuous batching vs 静态批处理 vs 串行 —— 推理优化 Step 4 进阶基准。

关键点
------
请求长度**参差不齐**时：
- 静态批处理（lockstep）必须等最长的请求一起结束，短请求的位置被浪费；
- continuous batching 让短请求提前结束、立即让位给新请求，batch 始终满载。

用法
----
.. code-block:: bash

    python 大模型/llm/cont_bench.py --train_steps 300 --n_requests 48
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

from llm.continuous import ContinuousBatchingEngine
from llm.serving import batched_generate
from llm.train_utils import encode, train_char_gpt

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
DATA_FILE = Path(__file__).resolve().parent.parent / "training_data.txt"

plt.switch_backend("Agg")  # 无显示环境下绘图


def sequential_time(model, requests):
    t0 = time.perf_counter()
    for prompt, max_new in requests:
        model.generate(prompt, max_new_tokens=max_new, use_kv_cache=True, sample=False)
    return time.perf_counter() - t0


def static_time(model, prompts, max_len, max_batch):
    """静态批处理：按 max_batch 分块，每块 lockstep 生成 max_len（不做 slot 复用）。"""
    t0 = time.perf_counter()
    for i in range(0, prompts.size(0), max_batch):
        chunk = prompts[i : i + max_batch]
        batched_generate(model, chunk, gen_len=max_len, sample=False)
    return time.perf_counter() - t0


def continuous_time(model, requests, max_batch):
    engine = ContinuousBatchingEngine(model, max_batch=max_batch)
    t0 = time.perf_counter()
    engine.serve(requests)
    return time.perf_counter() - t0


def main() -> None:
    parser = argparse.ArgumentParser(description="continuous batching 基准")
    parser.add_argument("--train_steps", type=int, default=300)
    parser.add_argument("--train_kb", type=int, default=50)
    parser.add_argument("--n_requests", type=int, default=48)
    parser.add_argument("--prompt_len", type=int, default=16)
    parser.add_argument("--min_len", type=int, default=3)
    parser.add_argument("--max_len", type=int, default=12)
    parser.add_argument("--max_batch", type=int, default=8)
    args = parser.parse_args()

    text = DATA_FILE.read_text(encoding="utf-8", errors="ignore")
    train_text = text[: args.train_kb * 1024]

    print("训练模型 ...")
    model, char_to_idx, _ = train_char_gpt(
        train_text, n_layer=2, n_embd=64, n_head=2, steps=args.train_steps, seq_len=128
    )

    # 构造请求：长度参差（模拟真实场景）
    torch.manual_seed(0)
    ids = encode(train_text, char_to_idx)
    prompts = []
    max_news = []
    step = max(1, len(ids) - args.prompt_len) // args.n_requests
    for i in range(args.n_requests):
        start = i * step
        prompts.append(
            torch.tensor(ids[start : start + args.prompt_len], dtype=torch.long).unsqueeze(0)
        )
        max_news.append(int(torch.randint(args.min_len, args.max_len + 1, (1,)).item()))
    prompts_all = torch.cat(prompts, dim=0)
    requests = list(zip(prompts, max_news))
    max_len = max(max_news)
    useful_tokens = sum(max_news)

    print("测量 ...")
    t_seq = sequential_time(model, requests)
    t_static = static_time(model, prompts_all, max_len, args.max_batch)
    t_cont = continuous_time(model, requests, args.max_batch)

    def eff_tps(t):
        return useful_tokens / t

    results = {
        "sequential": (t_seq, eff_tps(t_seq)),
        "static": (t_static, eff_tps(t_static)),
        "continuous": (t_cont, eff_tps(t_cont)),
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    labels = ["sequential", "static batch", "continuous batching"]
    times = [results[k][0] for k in ["sequential", "static", "continuous"]]
    plt.bar(labels, times, color=["#7f8c8d", "#2980b9", "#27ae60"])
    plt.ylabel("wall time (s)")
    plt.title("Varying-length requests: scheduling strategies")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    chart = REPORTS_DIR / "cont_batching.png"
    plt.savefig(chart, dpi=120)
    plt.close()

    report = (
        f"# continuous batching 基准\n\n"
        f"- 模型参数：`{model.num_params():,}`；请求 `{args.n_requests}`，"
        f"prompt `{args.prompt_len}`，长度均匀分布在 `[{args.min_len},{args.max_len}]`\n"
        f"- 有效 token 总数：`{useful_tokens}`\n\n"
        f"| 调度方式 | 墙钟 (s) | 有效吞吐 (tokens/s) |\n"
        f"|---------|----------|---------------------|\n"
        f"| sequential | {t_seq:.3f} | {eff_tps(t_seq):.0f} |\n"
        f"| static batch | {t_static:.3f} | {eff_tps(t_static):.0f} |\n"
        f"| **continuous batching** | {t_cont:.3f} | **{eff_tps(t_cont):.0f}** |\n\n"
        f"## 结论\n"
        f"- 长度参差时，静态批处理要等最长的请求，短请求的位置被浪费；\n"
        f"- continuous batching 让短请求提前结束并立即让位，batch 始终满载，"
        f"有效吞吐明显更高。\n"
    )
    md = REPORTS_DIR / "cont_report.md"
    md.write_text(report, encoding="utf-8")

    print(f"\n有效 token 总数: {useful_tokens}")
    for k, (t, tps) in results.items():
        print(f"  {k:12s}: {t:.3f}s  ({tps:.0f} tokens/s)")
    print(f"报告: {md}\n图表: {chart}")


if __name__ == "__main__":
    main()
