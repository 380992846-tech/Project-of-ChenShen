"""
download_models.py — 下载官方 Ising 预训练解码器

从 HuggingFace 下载 NVIDIA 官方的颜色代码预训练模型：
- fast（0.9M 参数，速度优化）
- accurate（1.8M 参数，精度优化）

用法：
    python scripts/download_models.py                # 下载 fast + accurate
    python scripts/download_models.py --size fast    # 只下 fast
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"

# 官方 HF 仓库（以 NVIDIA 实际发布为准）
HF_REPOS = {
    "fast": "nvidia/Ising-Decoder-ColorCode-1-Fast",
    "accurate": "nvidia/Ising-Decoder-ColorCode-1-Accurate",
}


def download(size: str) -> None:
    MODELS.mkdir(exist_ok=True)
    repo = HF_REPOS[size]
    print(f"[download] {size}: {repo}")
    try:
        from huggingface_hub import snapshot_download
        snapshot_download(repo_id=repo, local_dir=str(MODELS / size))
        print(f"[ok] 已下载到 {MODELS / size}")
    except Exception as e:
        print(f"[warn] 下载失败（需安装 huggingface_hub / 检查网络）: {e}")
        print(f"  可手动下载: https://huggingface.co/{repo}")


def main() -> None:
    p = argparse.ArgumentParser(description="下载官方 Ising 预训练解码器")
    p.add_argument("--size", choices=["fast", "accurate", "all"], default="all")
    args = p.parse_args()

    sizes = ["fast", "accurate"] if args.size == "all" else [args.size]
    for s in sizes:
        download(s)


if __name__ == "__main__":
    main()
