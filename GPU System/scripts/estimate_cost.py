#!/usr/bin/env python3
"""
训练成本估算工具（engineer 版经验公式）。

估算一次训练/微调的：
  - 总 FLOPs
  - 所需 GPU·小时
  - 云上算力成本（按每小时租金）
  - 电费（按平均功耗 × PUE × 电价）

公式：FLOPs ≈ 6 × Params(B) × Tokens(B)
      GPU_hours ≈ FLOPs / (单卡有效FLOPS × 并行效率)
      算力成本 ≈ GPU_hours × 时租
      电费     ≈ GPU_hours × 平均功耗(kW) × PUE × 电价($/kWh)
"""

import argparse

# 数据中心 PUE 预设（可快速套用；--pue 显式给出时以 --pue 为准）
DC_PRESETS = {
    "default": 1.30,
    "nmg": 1.15,           # 内蒙古：天然冷风，PUE 极低（本地算力中心的卖点）
    "zhongguancun": 1.70,  # 中关村：城市机房，PUE 偏高
}


def estimate(params_b, tokens_b, gpu_flops, efficiency, hours_rate,
             avg_kw, pue, price_kwh, network_loss=0.10):
    # 互联带宽瓶颈：MoE 千卡扩放时网络带宽可能吃掉一部分等效算力
    # 夹到 [0, 0.95] 以保证等效效率最小为原效率的 5%，避免除零
    loss = max(0.0, min(0.95, network_loss))
    eff = efficiency * (1.0 - loss)
    flops = 6.0 * params_b * 1e9 * tokens_b * 1e9
    gpu_hours = flops / (gpu_flops * eff)
    compute_cost = gpu_hours * hours_rate
    energy_kwh = gpu_hours * avg_kw * pue
    energy_cost = energy_kwh * price_kwh
    return {
        "flops": flops,
        "eff_effective": eff,
        "gpu_hours": gpu_hours,
        "compute_cost_usd": compute_cost,
        "energy_kwh": energy_kwh,
        "energy_cost_usd": energy_cost,
        "total_usd": compute_cost + energy_cost,
    }


def main():
    p = argparse.ArgumentParser(description="估算 LLM 训练/微调成本")
    p.add_argument("--params", type=float, default=7, help="参数量 (B, 十亿)")
    p.add_argument("--tokens", type=float, default=1000, help="训练 token (B, 十亿)")
    p.add_argument("--gpu", default="H100", help="GPU 型号: A100/H100/H200/B200（或自定义）")
    p.add_argument("--flops", type=float, help="单卡有效FLOPS (默认按型号)")
    p.add_argument("--eff", type=float, default=0.35, help="并行/计算效率 (0-1)")
    p.add_argument("--rate", type=float, help="GPU 每小时租金 (USD)")
    p.add_argument("--kw", type=float, default=0.5, help="训练平均功耗 (kW)")
    p.add_argument("--pue", type=float, help="数据中心 PUE（默认按 --dc，或 1.30）")
    p.add_argument("--dc", default="default", choices=list(DC_PRESETS),
                   help="数据中心预设: default/nmg(内蒙古低PUE)/zhongguancun(中关村高PUE)")
    p.add_argument("--network-loss", type=float, default=0.10,
                   help="互联带宽瓶颈导致的等效效率损失 (0-1)，默认 0.10")
    p.add_argument("--price", type=float, default=0.08, help="电价 (USD/kWh)")
    args = p.parse_args()

    gpu_map = {
        "A100": (312e12, 1.8),
        "H100": (989e12, 2.8),
        "H200": (989e12, 4.5),
        "B200": (2250e12, 6.0),
    }
    if args.flops:
        flops = args.flops
        rate = args.rate
    elif args.gpu.upper() in gpu_map:
        flops, rate = gpu_map[args.gpu.upper()]
    else:
        print(f"未知 GPU {args.gpu}，请用 --flops 和 --rate 指定")
        return
    if args.rate:
        rate = args.rate
    pue = args.pue if args.pue is not None else DC_PRESETS[args.dc]

    r = estimate(args.params, args.tokens, flops, args.eff, rate, args.kw, pue, args.price,
                 args.network_loss)

    print(f"GPU: {args.gpu} | params={args.params}B | tokens={args.tokens}B | "
          f"效率={args.eff} | 时租=${rate:.2f}")
    print("-" * 62)
    print(f"总 FLOPs         : {r['flops']:.3e}")
    print(f"等效效率(含互联) : {r['eff_effective']:.2f}  (基础 {args.eff:.2f} × (1-{args.network_loss:.2f}))")
    pue_label = "--pue 覆盖" if args.pue is not None else f"{args.dc} 预设"
    print(f"PUE (数据中心)   : {pue:.2f}  ({pue_label})")
    print(f"GPU·小时         : {r['gpu_hours']:,.0f}")
    print(f"算力成本 (租)    : ${r['compute_cost_usd']:,.0f}")
    print(f"电费             : ${r['energy_cost_usd']:,.0f}  ({r['energy_kwh']:,.0f} kWh)")
    print(f"合计(估)         : ${r['total_usd']:,.0f}")


if __name__ == "__main__":
    main()
