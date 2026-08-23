"""
benchmark.py
============

KV Cache vs 无 KV Cache 的**解码性能对比**。

衡量指标
--------
- 每 token 解码耗时（随序列增长：无 KV 呈 O(T)，有 KV 近似 O(1)）
- 生成速率（tokens/sec）
- 加速比
- （如有 GPU）峰值显存

产物
----
写入 ``大模型/llm/reports/``：
- ``kv_cache_speedup.png``  —— 每 token 耗时随生成步数变化的曲线
- ``kv_cache_report.md``     —— 结果报告

用法
----
.. code-block:: bash

    python 大模型/llm/benchmark.py \
        --n_layer 4 --n_embd 128 --n_head 4 \
        --prompt_len 64 --gen_len 128 --trials 3
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

from gpt import GPT, GPTConfig

REPORTS_DIR = Path(__file__).resolve().parent / "reports"

plt.switch_backend("Agg")  # 无显示环境下绘图


def _sync() -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def time_decode_step(model: GPT, idx: torch.Tensor, use_kv_cache: bool, past):
    """执行一步解码，返回 (耗时秒, 更新后的 past)。"""
    with torch.no_grad():
        _sync()
        t0 = time.perf_counter()
        input_ids = idx[:, -1:] if (use_kv_cache and past is not None) else idx
        _, past = model(input_ids, past if use_kv_cache else None)
        _sync()
        dt = time.perf_counter() - t0
    return dt, past


def _decode_once(model: GPT, prompt: torch.Tensor, gen_len: int, use_kv_cache: bool):
    """执行一轮解码，返回 (每步累计耗时列表, 总耗时, prefill 耗时)。"""
    cum = []
    past = None
    seq = prompt
    dt_sum = 0.0
    prefill_time = 0.0

    if use_kv_cache:
        with torch.no_grad():
            _sync()
            t0 = time.perf_counter()
            _, past = model(seq, None)  # prefill
            _sync()
            prefill_time = time.perf_counter() - t0

    for _ in range(gen_len):
        dt, past = time_decode_step(model, seq, use_kv_cache, past)
        dt_sum += dt
        cum.append(dt_sum)
        with torch.no_grad():
            if use_kv_cache:
                full_logits, _ = model(seq[:, -1:], past)
            else:
                full_logits, _ = model(seq)
        seq = torch.cat([seq, full_logits[:, -1:].argmax(dim=-1)], dim=1)

    return cum, dt_sum, prefill_time


def run_benchmark(cfg: GPTConfig, prompt_len: int, gen_len: int, trials: int) -> dict:
    torch.manual_seed(0)
    model = GPT(cfg).eval()
    prompt = torch.randint(0, cfg.vocab_size, (1, prompt_len))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    result = {"device": device, "params": model.num_params(), "cfg": cfg}

    # 预热
    for _ in range(2):
        time_decode_step(model, prompt, True, None)
        time_decode_step(model, prompt, False, None)

    # 多轮取平均，降低 CPU 计时噪声
    plain_cums, kv_cums, prefill_times = [], [], []
    for _ in range(trials):
        pc, p_total, _ = _decode_once(model, prompt, gen_len, use_kv_cache=False)
        kc, k_total, k_prefill = _decode_once(model, prompt, gen_len, use_kv_cache=True)
        plain_cums.append(pc)
        kv_cums.append(kc)
        prefill_times.append(k_prefill)

    # 逐 token 取平均
    plain_cum = [sum(r[i] for r in plain_cums) / trials for i in range(gen_len)]
    kv_cum = [sum(r[i] for r in kv_cums) / trials for i in range(gen_len)]
    plain_dt_sum = plain_cum[-1]
    kv_dt_sum = kv_cum[-1]
    prefill_time = sum(prefill_times) / trials

    # 每 token 平均耗时
    plain_per_tok = plain_dt_sum / gen_len
    kv_per_tok = kv_dt_sum / gen_len
    speedup = plain_dt_sum / kv_dt_sum if kv_dt_sum > 0 else float("nan")

    result.update(
        {
            "prompt_len": prompt_len,
            "gen_len": gen_len,
            "trials": trials,
            "prefill_time_s": prefill_time,
            "plain_decode_total_s": plain_dt_sum,
            "kv_decode_total_s": kv_dt_sum,
            "plain_per_token_ms": plain_per_tok * 1e3,
            "kv_per_token_ms": kv_per_tok * 1e3,
            "plain_tokens_per_sec": gen_len / plain_dt_sum,
            "kv_tokens_per_sec": gen_len / kv_dt_sum,
            "speedup_x": speedup,
            "plain_cum": plain_cum,
            "kv_cum": kv_cum,
        }
    )
    return result


def plot(result: dict, out_png: Path) -> None:
    gen_len = result["gen_len"]
    steps = list(range(1, gen_len + 1))
    plt.figure(figsize=(9, 5))
    plt.plot(steps, result["plain_cum"], label="without KV cache (O(T))", marker="o", ms=3)
    plt.plot(steps, result["kv_cum"], label="with KV cache (O(1) per step)", marker="s", ms=3)
    plt.xlabel("generated token index")
    plt.ylabel("cumulative decode time (s)")
    plt.title("KV Cache decode time comparison")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    plt.close()


def render_report(result: dict) -> str:
    cfg = result["cfg"]
    speedup = result["speedup_x"]
    return f"""# KV Cache 推理优化报告

## 环境
- 设备：`{result["device"]}`
- 模型：decoder-only GPT，参数 `{result["params"]:,}`
- 配置：`n_layer={cfg.n_layer}`, `n_head={cfg.n_head}`, `n_embd={cfg.n_embd}`
- 其他：`block_size={cfg.block_size}`, `vocab={cfg.vocab_size}`
- 实验：prompt 长度 `{result["prompt_len"]}`，生成 `{result["gen_len"]}` 个 token

## 结论
| 指标 | 无 KV Cache | 有 KV Cache |
|------|------------|-------------|
| 解码总耗时 (s) | {result["plain_decode_total_s"]:.4f} | {result["kv_decode_total_s"]:.4f} |
| 平均每 token 耗时 (ms) | {result["plain_per_token_ms"]:.3f} | {result["kv_per_token_ms"]:.3f} |
| 生成速率 (tokens/s) | {result["plain_tokens_per_sec"]:.1f} | {result["kv_tokens_per_sec"]:.1f} |
| **加速比** | 1.0× | **{speedup:.2f}×** |

- prefill 耗时（一次性处理 prompt）：`{result["prefill_time_s"] * 1e3:.2f} ms`

## 说明
- 无 KV Cache 时每步都要对全部历史 token 重新做一次注意力，单步耗时随序列增长（O(T)）。
- 有 KV Cache 时 K/V 在 prefill 阶段算好并缓存，decode 每步只处理 1 个新 token（O(1)），
  单步耗时近似恒定，总耗时随生成步数**线性**而非**平方**增长。
- 本报告用随机权重模型演示**算法层面的复杂度差异**；真实加速比还取决于
  显存带宽、批大小与算子实现（如 FlashAttention / vLLM）。
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="KV Cache 解码性能对比")
    parser.add_argument("--vocab_size", type=int, default=256)
    parser.add_argument("--n_layer", type=int, default=4)
    parser.add_argument("--n_head", type=int, default=4)
    parser.add_argument("--n_embd", type=int, default=128)
    parser.add_argument("--block_size", type=int, default=512)
    parser.add_argument("--prompt_len", type=int, default=64)
    parser.add_argument("--gen_len", type=int, default=128)
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    cfg = GPTConfig(
        vocab_size=args.vocab_size,
        n_layer=args.n_layer,
        n_head=args.n_head,
        n_embd=args.n_embd,
        block_size=args.block_size,
    )

    result = run_benchmark(cfg, args.prompt_len, args.gen_len, args.trials)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    png = REPORTS_DIR / "kv_cache_speedup.png"
    md = REPORTS_DIR / "kv_cache_report.md"
    plot(result, png)
    report = render_report(result)
    md.write_text(report, encoding="utf-8")

    print(f"设备: {result['device']} | 参数量: {result['params']:,}")
    print(
        f"加速比: {result['speedup_x']:.2f}x  "
        f"({result['plain_tokens_per_sec']:.1f} -> {result['kv_tokens_per_sec']:.1f} tokens/s)"
    )
    print(f"报告: {md}")
    print(f"图表: {png}")


if __name__ == "__main__":
    main()
