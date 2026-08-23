"""权重量化（quantize.py）测试。"""

import torch

from quantize import GROUP_SIZE, quantize_weight_tensor


def _w(rows=8, cols=64):
    return torch.randn(rows, cols) * 2.0


def test_fp32_identity():
    w = _w()
    dq, stored, err = quantize_weight_tensor(w, 32)
    assert err == 0.0
    assert torch.allclose(dq, w)
    assert stored == w.numel() * 4


def test_int8_small_error_and_storage():
    w = _w()
    _, stored, err = quantize_weight_tensor(w, 8)
    assert err < 0.5          # 8bit 还原误差很小
    assert stored == w.numel() + 4


def test_int4_groupwise_storage():
    w = _w(rows=8, cols=64)   # inn=64 能被 GROUP_SIZE(32) 整除
    _, stored, err = quantize_weight_tensor(w, 4, group_size=GROUP_SIZE)
    assert stored < w.numel()  # 每权重 < 1 字节
    assert err < 1.0


def test_fp8_storage():
    w = _w()
    _, stored, _ = quantize_weight_tensor(w, "fp8")
    assert stored == w.numel()


def test_invalid_bits_raises():
    w = _w()
    try:
        quantize_weight_tensor(w, 16)
    except ValueError:
        return
    raise AssertionError("should raise ValueError for unsupported bits")
