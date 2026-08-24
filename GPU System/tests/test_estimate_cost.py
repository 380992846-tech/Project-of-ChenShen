import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from estimate_cost import DC_PRESETS, estimate


def test_estimate_applies_network_loss():
    r = estimate(671, 14800, 989e12, 0.35, 2.8, 0.5, 1.15, 0.08, network_loss=0.2)
    assert abs(r["eff_effective"] - (0.35 * 0.8)) < 1e-9
    assert r["gpu_hours"] > 0
    assert r["total_usd"] > 0


def test_estimate_zero_network_loss_matches_base():
    r = estimate(7, 1000, 312e12, 0.35, 1.8, 0.5, 1.3, 0.08, network_loss=0.0)
    assert abs(r["eff_effective"] - 0.35) < 1e-9
    assert r["compute_cost_usd"] > 0
    assert r["total_usd"] > 0


def test_network_loss_clamped():
    # 超过 1 时被夹到 0.95，等效效率最小为 0.05 × 原效率，避免除零
    r = estimate(7, 1000, 312e12, 0.35, 1.8, 0.5, 1.3, 0.08, network_loss=5)
    assert abs(r["eff_effective"] - (0.35 * 0.05)) < 1e-9
    assert r["gpu_hours"] > 0


def test_dc_presets_order():
    # 内蒙古天然冷风 PUE 应显著低于中关村城市机房
    assert DC_PRESETS["nmg"] < DC_PRESETS["default"] < DC_PRESETS["zhongguancun"]
