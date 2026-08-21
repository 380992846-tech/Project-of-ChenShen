"""
quantize.py
===========

GPT 的**权重量化**工具，用于推理优化 Step 2：对比不同精度下的
存储占用、权重复原误差、输出 logit 偏差与困惑度（PPL）。

支持模式
--------
- ``bits=32`` ：FP32 基线
- ``bits=8``  ：INT8（对称，1 字节/权重）
- ``bits=4``  ：INT4 分组（group-wise，非对称，≈0.5–0.75 字节/权重）
- ``bits="fp8"``：FP8 (e4m3fn，1 字节/权重，torch 模拟)

说明
----
INT4 / FP8 采用 **weight-only** 量化：以低精度存储权重，计算时反量化回 FP32。
这样能准确度量**权重精度损失**对输出的影响与**显存节省**；而真正的
INT4/FP8 计算加速依赖 GPU 上的专用算子（如 Marlin / Triton），CPU 上不做虚假加速宣称。
INT8 额外提供 torch 原生动态量化（``quantize_dynamic``）的运行时版本。
"""

from __future__ import annotations

import copy
from dataclasses import dataclass

import torch
import torch.nn as nn

from llm.gpt import GPT

GROUP_SIZE = 32


@dataclass
class QuantResult:
    """一次量化评估的结果。"""

    mode: str
    stored_bytes: int
    stored_mb: float
    weight_recon_error: float
    logit_deviation: float
    ppl: float | None
    decode_ms_per_token: float | None


def quantize_weight_tensor(w: torch.Tensor, bits, group_size: int = GROUP_SIZE):
    """对单个权重张量做 weight-only 量化。

    Returns:
        (反量化后的 fp32 权重, 存储字节数, 最大绝对还原误差)
    """
    if bits == 32:
        return w.clone(), w.numel() * 4, 0.0

    if bits == 8:
        scale = w.abs().max() / 127.0
        q = torch.clamp(torch.round(w / scale).to(torch.int8), -128, 127)
        dq = q.to(torch.float32) * scale
        err = (w - dq).abs().max().item()
        # 1 字节/权重 + 少量 scale
        stored = w.numel() + 4
        return dq, int(stored), err

    if bits == 4:
        out, inn = w.shape
        assert inn % group_size == 0, "inn 需能被 group_size 整除"
        wg = w.reshape(out, inn // group_size, group_size)
        wmin = wg.min(dim=-1, keepdim=True).values
        wmax = wg.max(dim=-1, keepdim=True).values
        scale = (wmax - wmin) / 15.0
        scale = torch.where(scale == 0, torch.ones_like(scale), scale)
        q = torch.clamp(torch.round((wg - wmin) / scale), 0, 15)
        dq = (q.to(torch.float32) * scale + wmin).reshape(out, inn)
        err = (w - dq).abs().max().item()
        # 权重 0.5 字节 + 每组 scale(4B)+zero(4B)
        n_groups = (inn // group_size) * out
        stored = int(w.numel() * 0.5 + n_groups * 8)
        return dq, stored, err

    if bits == "fp8":
        w8 = w.to(torch.float8_e4m3fn)
        dq = w8.to(torch.float32)
        err = (w - dq).abs().max().item()
        return dq, int(w.numel()), err

    raise ValueError(f"不支持的 bits: {bits!r}")


def make_quantized_model(model: GPT, bits, group_size: int = GROUP_SIZE) -> GPT:
    """返回权重被量化的模型深拷贝（计算用反量化后的权重）。

    只量化二维权重矩阵（Linear / Embedding），LayerNorm 等一维参数保持 FP32。
    """
    m = copy.deepcopy(model).eval()
    for name, p in m.named_parameters():
        if p.dim() >= 2:
            dq, _, _ = quantize_weight_tensor(p.data, bits, group_size)
            p.data.copy_(dq)
    return m


def quantized_memory(model: GPT, bits, group_size: int = GROUP_SIZE) -> int:
    """统计该精度下的权重存储字节数（仅二维权重矩阵）。"""
    total = 0
    for p in model.parameters():
        if p.dim() >= 2:
            _, stored, _ = quantize_weight_tensor(p.data, bits, group_size)
            total += stored
        else:
            total += p.numel() * 4  # 一维参数按 FP32 计
    return total


def make_int8_dynamic(model: GPT) -> GPT:
    """torch 原生动态 INT8 量化（运行时真实 int8 算子）。"""
    m = copy.deepcopy(model).eval()
    return torch.quantization.quantize_dynamic(m, {nn.Linear}, dtype=torch.qint8)
