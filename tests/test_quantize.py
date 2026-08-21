"""量化模块的单元测试。"""

import torch
from llm.gpt import GPT, GPTConfig
from llm.quantize import (
    make_int8_dynamic,
    make_quantized_model,
    quantize_weight_tensor,
    quantized_memory,
)


def _random_weight(out=64, inn=64, seed=0):
    torch.manual_seed(seed)
    return torch.randn(out, inn) * 2.0


def test_int8_reconstruction_small_error():
    w = _random_weight()
    dq, stored, err = quantize_weight_tensor(w, 8)
    assert err < 0.1
    assert stored <= w.numel() + 8


def test_int4_memory_less_than_int8():
    w = _random_weight(out=64, inn=64)
    _, s8, _ = quantize_weight_tensor(w, 8)
    _, s4, _ = quantize_weight_tensor(w, 4)
    _, sfp8, _ = quantize_weight_tensor(w, "fp8")
    assert s4 < s8
    assert sfp8 < s8
    # 存储单调：fp32 > int8 ≈ fp8 > int4
    assert w.numel() * 4 > s8


def test_quantized_model_forward_shapes():
    torch.manual_seed(1)
    cfg = GPTConfig(vocab_size=64, n_layer=2, n_head=2, n_embd=32, block_size=64)
    model = GPT(cfg).eval()
    x = torch.randint(0, 64, (1, 20))
    for bits in [8, 4, "fp8"]:
        q = make_quantized_model(model, bits)
        logits, _ = q(x)
        assert logits.shape == (1, 20, 64)


def test_int8_dynamic_runs():
    torch.manual_seed(2)
    cfg = GPTConfig(vocab_size=64, n_layer=2, n_head=2, n_embd=32, block_size=64)
    model = GPT(cfg).eval()
    q = make_int8_dynamic(model)
    x = torch.randint(0, 64, (1, 20))
    logits, _ = q(x)
    assert logits.shape == (1, 20, 64)


def test_int8_dynamic_memory_smaller():
    torch.manual_seed(3)
    cfg = GPTConfig(vocab_size=64, n_layer=2, n_head=2, n_embd=32, block_size=64)
    model = GPT(cfg).eval()
    assert quantized_memory(model, 8) < quantized_memory(model, 32)
