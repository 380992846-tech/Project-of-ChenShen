#!/usr/bin/env python3
"""绘制 GEAR 功耗曲线：空闲 vs 推理负载（两张 collect_power 的 CSV）。

用法：
    python scripts/plot_power_curve.py --idle p_curve.csv --load p_load2.csv --out docs/images/power_curve.png
"""

from __future__ import annotations

import argparse
import csv
import os


def load(path: str) -> tuple[list[float], list[float]]:
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    t0 = float(rows[0]["t"])
    ts = [float(r["t"]) - t0 for r in rows]
    pw = [float(r["power_w"]) for r in rows]
    return ts, pw


def main() -> int:
    ap = argparse.ArgumentParser(description="绘制空闲 vs 负载功耗曲线")
    ap.add_argument("--idle", required=True, help="空闲/基线功耗 CSV")
    ap.add_argument("--load", required=True, help="负载功耗 CSV")
    ap.add_argument("--out", default="docs/images/power_curve.png", help="输出 PNG")
    args = ap.parse_args()

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ts_i, pw_i = load(args.idle)
    ts_l, pw_l = load(args.load)
    avg_i = sum(pw_i) / len(pw_i)
    avg_l = sum(pw_l) / len(pw_l)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ts_i, pw_i, label=f"Idle (avg {avg_i:.0f} W)", color="#7a4bff", lw=1.6)
    ax.plot(ts_l, pw_l, label=f"vLLM inference (avg {avg_l:.0f} W)", color="#f7c948", lw=1.6)
    ax.axhline(avg_l, color="#f7c948", ls="--", alpha=0.4)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("GPU power (W)")
    ax.set_title("GEAR · NVIDIA A800 — idle vs vLLM inference power")
    ax.grid(alpha=0.3)
    ax.legend()

    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    fig.savefig(args.out, dpi=150)
    plt.close()
    print(f"saved {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
