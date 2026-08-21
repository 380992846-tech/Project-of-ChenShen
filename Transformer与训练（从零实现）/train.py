"""
train.py — 在真实中文语料上训练字符级 GPT（GPU / CPU / 分布式）

相比旧版（CPU 单机），本版本升级：
- **GPU 支持**：``device = cuda if available else cpu``，数据与模型自动迁移；
- **DistributedDataParallel (DDP)**：多卡/多机并行训练；
- **config.yaml 实验管理**：超参数从 YAML 加载，命令行 ``--key value`` 可覆盖；
- 训练中记录 train/val 损失、困惑度，保存最佳 checkpoint；
- 训练中/结束后生成中文样例，输出损失曲线与 `训练报告.md`。

用法
----
.. code-block:: bash

    # CPU 训练
    python train.py --config config.yaml

    # 单 GPU
    python train.py --config config.yaml

    # 多 GPU 分布式（torchrun）
    torchrun --nproc_per_node=2 train.py --config config.yaml

    # 命令行覆盖超参数
    python train.py --steps 3000 --n_embd 192 --n_layer 6
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

# Windows 控制台默认 GBK，遇非 GBK 字符（如生成文本中的 \xa0）print 会抛 UnicodeEncodeError。
# 强制 stdout/stderr 使用 UTF-8 并容错替换，保证训练打印中文不中断。
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP

# 保证能 import 项目内的 models / data 包
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from data.dataset import CharDataset, build_vocab, decode, encode  # noqa: E402
from models.config import Config, load_config  # noqa: E402
from models.gpt import GPT, GPTConfig  # noqa: E402

plt.switch_backend("Agg")

MODELS_DIR = HERE / "checkpoints"
DATA_FILE = HERE / "training_data.txt"


# --------------------------------------------------------------------------
# 分布式工具
# --------------------------------------------------------------------------
def is_distributed() -> bool:
    return dist.is_available() and dist.is_initialized()


def is_main_process() -> bool:
    return not is_distributed() or dist.get_rank() == 0


def get_device() -> torch.device:
    """GPU 优先，否则 CPU。"""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def setup_distributed() -> None:
    """当通过 torchrun 启动时初始化进程组。"""
    local_rank = int(os.environ.get("LOCAL_RANK", "-1"))
    if local_rank >= 0 and dist.is_available():
        dist.init_process_group(backend="nccl" if torch.cuda.is_available() else "gloo")
        torch.cuda.set_device(local_rank)


def cleanup_distributed() -> None:
    if is_distributed():
        dist.destroy_process_group()


# --------------------------------------------------------------------------
# 训练
# --------------------------------------------------------------------------
def save_checkpoint(model: GPT, cfg: GPTConfig, path: Path) -> None:
    """保存 state_dict + 模型配置，便于 generate.py 精确恢复结构。"""
    torch.save({"model": model.state_dict(), "config": asdict(cfg)}, path)


def get_batch(data: torch.Tensor, batch: int, seq_len: int, device: torch.device):
    """随机采样一批 (x, y) 序列。"""
    ix = torch.randint(0, len(data) - seq_len - 1, (batch,))
    xb = torch.stack([data[i : i + seq_len] for i in ix])
    yb = torch.stack([data[i + 1 : i + seq_len + 1] for i in ix])
    return xb.to(device), yb.to(device)


def train(args) -> dict:
    setup_distributed()
    device = get_device()
    torch.manual_seed(args.seed)

    cfg = load_config(args.config)
    # 命令行覆盖：显式映射到对应配置节
    _TRAIN_OVERRIDES = {
        "steps": "steps", "batch": "batch", "lr": "lr",
        "eval_every": "eval_every", "gen_len": "gen_len", "seed": "seed",
    }
    _MODEL_OVERRIDES = {
        "n_embd": "n_embd", "n_layer": "n_layer", "n_head": "n_head",
    }
    _DATA_OVERRIDES = {"seq_len": "seq_len", "tokenizer": "tokenizer"}

    for cli_key, cfg_key in _TRAIN_OVERRIDES.items():
        val = getattr(args, cli_key, None)
        if val is not None:
            setattr(cfg.train, cfg_key, val)
    for cli_key, cfg_key in _MODEL_OVERRIDES.items():
        val = getattr(args, cli_key, None)
        if val is not None:
            setattr(cfg.model, cfg_key, val)
    for cli_key, cfg_key in _DATA_OVERRIDES.items():
        val = getattr(args, cli_key, None)
        if val is not None:
            setattr(cfg.data, cfg_key, val)

    # ---- 数据 ----
    text = DATA_FILE.read_text(encoding="utf-8", errors="ignore")
    tokenizer = getattr(cfg.data, "tokenizer", "char")
    if tokenizer == "bpe":
        # BPE 分词：先从语料训练临时词表（教学级），词表大小由 config 指定
        from data.bpe import BPETokenizer
        bpe = BPETokenizer.train(text, vocab_size=getattr(cfg.data, "bpe_vocab_size", 2000))
        char_to_idx, idx_to_char = bpe.vocab, bpe.id_to_token
        vocab = len(char_to_idx)
        cfg.model.vocab_size = vocab
        data = torch.tensor(bpe.encode(text), dtype=torch.long)

        def decode_fn(ids):
            # 用 BPE 解码，并把空格占位符 ▁ 还原为空格
            return bpe.decode(ids)
    else:
        char_to_idx, idx_to_char = build_vocab(text)
        vocab = len(char_to_idx)
        cfg.model.vocab_size = vocab  # 词表大小由语料决定
        data = encode(text, char_to_idx)
        decode_fn = lambda ids: decode(ids, idx_to_char)  # noqa: E731

    n_val = int(len(data) * cfg.data.val_ratio)
    train_data, val_data = data[:-n_val], data[-n_val:]
    if is_main_process():
        print(
            f"语料 {len(data)} 字符 | 词表 {vocab} | "
            f"train {len(train_data)} / val {len(val_data)} | device {device}"
        )

    # ---- 模型 ----
    gpt_cfg = GPTConfig(**asdict(cfg.model))
    model = GPT(gpt_cfg)
    model.to(device)

    if is_distributed():
        model = DDP(model, device_ids=[device.index] if device.index is not None else None)
    raw_model = model.module if isinstance(model, DDP) else model

    opt = torch.optim.AdamW(raw_model.parameters(), lr=cfg.train.lr)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # ---- TensorBoard（可选）：--log-dir 填写则实时记录损失曲线 ----
    writer = None
    if getattr(args, "log_dir", None) and is_main_process():
        try:
            from torch.utils.tensorboard import SummaryWriter
            writer = SummaryWriter(log_dir=args.log_dir)
            print(f"[tb] TensorBoard 日志目录: {args.log_dir}（tensorboard --logdir {args.log_dir}）")
        except Exception as e:
            print(f"[tb] 跳过 TensorBoard（{type(e).__name__}: {e}）")

    def eval_split(split: str) -> float:
        raw_model.eval()
        d = train_data if split == "train" else val_data
        losses = []
        with torch.no_grad():
            for _ in range(20):
                xb, yb = get_batch(d, cfg.train.batch, cfg.data.seq_len, device)
                logits, _ = model(xb)
                loss = F.cross_entropy(logits.reshape(-1, vocab), yb.reshape(-1))
                losses.append(loss.item())
        raw_model.train()
        return sum(losses) / len(losses)

    @torch.no_grad()
    def generate_sample(seed_str: str = "清华") -> tuple[str, str]:
        """返回 (提示词, 生成纯文本)，便于报告准确展示。"""
        raw_model.eval()
        start = [char_to_idx.get(c, 0) for c in seed_str]
        x = torch.tensor([start], dtype=torch.long, device=device)
        out = raw_model.generate(
            x, max_new_tokens=cfg.train.gen_len, use_kv_cache=True,
            sample=True, temperature=0.8,
        )
        raw_model.train()
        return seed_str, decode_fn(out[0])

    # ---- 训练循环 ----
    history = {"train": [], "val": []}
    best_val = float("inf")
    t0 = time.time()
    for step in range(1, cfg.train.steps + 1):
        xb, yb = get_batch(train_data, cfg.train.batch, cfg.data.seq_len, device)
        opt.zero_grad()
        logits, _ = model(xb)
        loss = F.cross_entropy(logits.reshape(-1, vocab), yb.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(raw_model.parameters(), cfg.train.grad_clip)
        opt.step()

        if step % cfg.train.eval_every == 0 or step == cfg.train.steps:
            m = {"train": eval_split("train"), "val": eval_split("val")}
            history["train"].append((step, m["train"]))
            history["val"].append((step, m["val"]))
            if writer is not None:
                writer.add_scalars("loss", {"train": m["train"], "val": m["val"]}, step)
                writer.add_scalar("ppl", math.exp(m["val"]), step)
            ppl = math.exp(m["val"])
            if m["val"] < best_val:
                best_val = m["val"]
                save_checkpoint(raw_model, gpt_cfg, MODELS_DIR / "best_char_gpt.pth")
            sample = generate_sample()
            el = time.time() - t0
            if is_main_process():
                print(
                    f"[{step}/{cfg.train.steps}] train {m['train']:.3f} | "
                    f"val {m['val']:.3f} | PPL {ppl:.1f} | {el:.0f}s"
                )
                print(f"    生成: {(sample[0] + sample[1])[:80]}")

    # ---- 最终 ----
    final = {"train": eval_split("train"), "val": eval_split("val")}
    if is_main_process():
        save_checkpoint(raw_model, gpt_cfg, MODELS_DIR / "final_char_gpt.pth")
        with open(MODELS_DIR / "vocab_char.json", "w", encoding="utf-8") as f:
            json.dump(char_to_idx, f, ensure_ascii=False)
        print(
            f"\n最终 train {final['train']:.3f} / val {final['val']:.3f} / "
            f"PPL {math.exp(final['val']):.1f}"
        )

        # 损失曲线
        plt.figure(figsize=(8, 5))
        plt.plot([s for s, _ in history["train"]], [v for _, v in history["train"]], label="train")
        plt.plot([s for s, _ in history["val"]], [v for _, v in history["val"]], label="val")
        plt.xlabel("step"); plt.ylabel("loss"); plt.title("Char-level GPT training loss")
        plt.legend(); plt.grid(alpha=.3)
        plt.tight_layout(); plt.savefig(HERE / "training_curve.png", dpi=120); plt.close()

        samples = [generate_sample(s) for s in cfg.train.sample_prompts]
        if writer is not None:
            writer.close()
        cleanup_distributed()
        return {
            "cfg": gpt_cfg, "vocab": vocab, "steps": cfg.train.steps,
            "final": final, "ppl": math.exp(final["val"]),
            "history": history, "samples": samples,
        }
    return {}


def write_report(result: dict) -> None:
    if not result:
        return
    cfg = result["cfg"]
    lines = [
        "# 字符级 GPT 训练报告（从零实现）",
        "",
        f"- 语料：`training_data.txt`（中文）| 字符词表 `{result['vocab']}`",
        f"- 模型：decoder-only GPT，`{cfg.n_layer}` 层 × `{cfg.n_embd}` 维 × `{cfg.n_head}` 头，block `{cfg.block_size}`",
        f"- 训练：`{result['steps']}` 步 | 最终 train loss `{result['final']['train']:.3f}` / val `{result['final']['val']:.3f}`",
        f"- **困惑度 PPL：`{result['ppl']:.1f}`**（越低越好；字符级随机基线 ≈ 词表大小 `{result['vocab']}`）",
        "",
        "## 训练损失",
        "",
        "| step | train loss | val loss |",
        "|------|-----------|----------|",
    ]
    for s, tl in result["history"]["train"]:
        vl = next(v for ss, v in result["history"]["val"] if ss == s)
        lines.append(f"| {s} | {tl:.3f} | {vl:.3f} |")
    lines += ["", "![损失曲线](training_curve.png)", "", "## 生成样例（训练后）", ""]
    for prompt, text in result["samples"]:
        lines.append(f"- 提示「{prompt}」→ **{prompt}{text}**")
    lines += [
        "",
        "## 结论",
        "",
        "- 从零实现的 decoder-only Transformer 能在真实中文语料上训练，损失持续下降、困惑度远低于随机基线；",
        "- 小模型 + CPU + 有限步数下，生成的是**短句级的通顺片段**；增大模型/语料/步数（或 GPU）可显著提升；",
        "- checkpoint 与词表存到 `checkpoints/`，可用 `generate.py` 加载做推理。",
    ]
    (HERE / "训练报告.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n报告已写入: {HERE / '训练报告.md'}")


def main() -> None:
    p = argparse.ArgumentParser(description="训练字符级 GPT（GPU / CPU / DDP）")
    p.add_argument("--config", type=str, default="config.yaml", help="YAML 配置文件")
    p.add_argument("--steps", type=int, default=None)
    p.add_argument("--n_embd", type=int, default=None)
    p.add_argument("--n_layer", type=int, default=None)
    p.add_argument("--n_head", type=int, default=None)
    p.add_argument("--seq_len", type=int, default=None)
    p.add_argument("--batch", type=int, default=None)
    p.add_argument("--lr", type=float, default=None)
    p.add_argument("--eval_every", type=int, default=None)
    p.add_argument("--gen_len", type=int, default=None)
    p.add_argument("--tokenizer", type=str, default=None, choices=["char", "bpe"],
                   help="分词方式：char 字符级 | bpe BPE 子词")
    p.add_argument("--log-dir", type=str, default=None,
                   help="TensorBoard 日志目录（可选，填了则实时记录损失曲线）")
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    # seed 默认取自 config.yaml
    if args.seed is None:
        args.seed = load_config(args.config).train.seed

    result = train(args)
    if is_main_process():
        write_report(result)


if __name__ == "__main__":
    main()
