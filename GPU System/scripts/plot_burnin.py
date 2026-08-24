#!/usr/bin/env python3
"""绘制 burn_in 的「矩阵规模 vs 功耗」散点（展示算力-功耗正相关）。

用法：
    python scripts/plot_burnin.py --csv burn_in.csv --out docs/images/burnin_power.png
"""

from __future__ import annotations

import argparse
import csv
import os


def main() -> int:
    ap = argparse.ArgumentParser(description="绘制烧机 算力-功耗 散点")
    ap.add_argument("--csv", required=True, help="burn_in.py 输出的 CSV")
    ap.add_argument("--out", default="docs/images/burnin_power.png", help="输出 PNG")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv, encoding="utf-8")))
    xs = [int(r["matrix_size"]) for r in rows]
    ys = [float(r["power_w"]) for r in rows]

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, "o-", color="#f7c948", lw=2, ms=8)
    ax.set_xlabel("matrix size (compute ↑)")
    ax.set_ylabel("GPU power (W)")
    ax.set_title("GEAR · NVIDIA A800 burn-in — compute ↑ → power ↑")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    fig.savefig(args.out, dpi=150)
    plt.close()
    print(f"saved {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
