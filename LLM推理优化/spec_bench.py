"""
spec_bench.py
=============

投机解码（Speculative Decoding）吞吐基准 —— 推理优化 Step 3。

流程
----
1. 用同一份中文语料训练一个**较大的 target 模型**与一个**较小的 draft 模型**；
2. 对比两种解码方式生成等量 token 的吞吐：
   - 目标模型自回归（KV Cache）；
   - 投机解码（draft 草稿 + target 一次并行验证）；
3. 度量：生成速率、平均每轮接受草稿数、墙钟加速比。

用法
----
.. code-block:: bash

    python 大模型/llm/spec_bench.py --train_steps 300
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
from speculative import speculative_decode
from train_utils import encode, train_char_gpt

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
DATA_FILE = Path(__file__).resolve().parent.parent / "training_data.txt"

plt.switch_backend("Agg")  # 无显示环境下绘图


@torch.no_grad()
def target_decode_speed(model: GPT, prompt: torch.Tensor, gen_len: int, warmup: int = 3) -> float:
    """目标模型自回归（KV Cache）生成 gen_len 个 token，返回 tokens/sec。"""
    model.eval()
    past = None
    seq = prompt
    for _ in range(warmup):
        if past is None:
            _, past = model(seq, None)
        else:
            _, past = model(seq[:, -1:], past)
    past = None
    seq = prompt
    t0 = time.perf_counter()
    for _ in range(gen_len):
        input_ids = seq if past is None else seq[:, -1:]
        logits, past = model(input_ids, past)
        seq = torch.cat([seq, logits[:, -1:].argmax(dim=-1)], dim=1)
    dt = time.perf_counter() - t0
    return gen_len / dt


def speculative_speed(draft, target, prompt, gamma, gen_len):
    """投机解码：返回 (tokens/sec, 平均每次验证产出的 token 数)。"""
    # 预热
    speculative_decode(draft, target, prompt, gamma=gamma, max_new_tokens=8, sample=False)

    # 计时（分块，避免单次过长）
    t0 = time.perf_counter()
    total = 0
    while total < gen_len:
        seg = speculative_decode(
            draft,
            target,
            prompt,
            gamma=gamma,
            max_new_tokens=min(gen_len - total, 32),
            sample=False,
        )
        total += seg.size(1)
    dt = time.perf_counter() - t0
    tps = total / dt

    # 平均每次验证产出的 token 数（投机收益的核心指标）
    _, stats = speculative_decode(
        draft,
        target,
        prompt,
        gamma=gamma,
        max_new_tokens=gen_len,
        sample=False,
        return_stats=True,
    )
    return tps, stats["avg_tokens_per_verification"]


def main() -> None:
    parser = argparse.ArgumentParser(description="投机解码吞吐基准")
    parser.add_argument("--train_steps", type=int, default=300)
    parser.add_argument("--train_kb", type=int, default=60)
    parser.add_argument("--gen_len", type=int, default=96)
    parser.add_argument("--gamma", type=int, default=4)
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    text = DATA_FILE.read_text(encoding="utf-8", errors="ignore")
    train_text = text[: args.train_kb * 1024]

    print("训练 target 模型 ...")
    target, char_to_idx, _ = train_char_gpt(
        train_text, n_layer=4, n_embd=128, n_head=4, steps=args.train_steps, seq_len=256
    )
    print("训练 draft 模型 ...")
    draft, char_to_idx2, _ = train_char_gpt(
        train_text, n_layer=1, n_embd=32, n_head=2, steps=args.train_steps, seq_len=256
    )
    # 对齐词汇表
    if char_to_idx != char_to_idx2:
        assert set(char_to_idx) == set(char_to_idx2), "词表不一致"

    prompt_ids = torch.tensor(
        encode(train_text[:64], char_to_idx)[:32], dtype=torch.long
    ).unsqueeze(0)

    print("测量吞吐（多次取平均）...")
    target_tps = []
    spec_tps = []
    avg_accept = None
    for _ in range(args.trials):
        target_tps.append(target_decode_speed(target, prompt_ids, args.gen_len))
        st, aa = speculative_speed(draft, target, prompt_ids, args.gamma, args.gen_len)
        spec_tps.append(st)
        avg_accept = aa
    target_tps = sum(target_tps) / args.trials
    spec_tps = sum(spec_tps) / args.trials
    speedup = spec_tps / target_tps
    # 算法层面的稳定指标：每个 token 需要的 target 前向调用次数
    target_fwd_per_token = 1.0
    spec_fwd_per_token = 1.0 / avg_accept if avg_accept else float("nan")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 图表
    plt.figure(figsize=(8, 5))
    plt.bar(
        ["target (KV cache)", f"speculative (γ={args.gamma})"],
        [target_tps, spec_tps],
        color=["#2c3e50", "#27ae60"],
    )
    plt.ylabel("tokens/sec")
    plt.title("Speculative Decoding throughput")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    chart = REPORTS_DIR / "spec_speedup.png"
    plt.savefig(chart, dpi=120)
    plt.close()

    report = (
        f"# 投机解码吞吐基准\n\n"
        f"- target 参数：`{target.num_params():,}`；draft 参数：`{draft.num_params():,}`\n"
        f"- 生成 `{args.gen_len}` token，`γ={args.gamma}`，`{args.trials}` 轮取平均\n\n"
        f"| 方式 | 吞吐 (tokens/s) | 每 token 的 target 前向次数 |\n"
        f"|------|-----------------|------------------------------|\n"
        f"| target (KV cache) | {target_tps:.1f} | {target_fwd_per_token:.2f} |\n"
        f"| speculative | {spec_tps:.1f} | {spec_fwd_per_token:.2f} |\n\n"
        f"**墙钟加速比**：{speedup:.2f}×（CPU 小模型，波动较大）\n\n"
        f"## 关键指标\n"
        f"- 平均每轮接受草稿数：**{avg_accept:.2f}**（最高 γ+1={args.gamma + 1}）\n"
        f"- **每 token 的 target 前向次数**：投机把 target 前向从每个 token 1 次降到"
        f" {spec_fwd_per_token:.2f} 次——这是与 GPU 无关的**算法层收益**，"
        f"在真实大模型上直接对应 ~{(1.0 / spec_fwd_per_token):.1f}× 的 target 计算量下降。\n\n"
        f"## 说明\n"
        f"- 投机解码用更快的 draft 猜 `γ` 个候选，target 一次并行验证，接受率越高，"
        f"每轮 target 前向产出的 token 越多；\n"
        f"- 墙钟加速取决于 **draft 相对 target 的加速比** × **接受率**："
        f"draft 不够快（如 CPU 小模型）时墙钟收益有限且噪声大；\n"
        f"- 正确性由精确拒绝采样保证（draft==target 时输出与 target 完全一致，测试覆盖）。\n"
    )
    md = REPORTS_DIR / "spec_report.md"
    md.write_text(report, encoding="utf-8")

    print(f"\n参数量: target {target.num_params():,}, draft {draft.num_params():,}")
    print(f"target 吞吐: {target_tps:.1f} tokens/s")
    print(f"speculative 吞吐: {spec_tps:.1f} tokens/s  (平均接受 {avg_accept:.2f})")
    print(f"加速比: {speedup:.2f}x")
    print(f"报告: {md}\n图表: {chart}")


if __name__ == "__main__":
    main()
