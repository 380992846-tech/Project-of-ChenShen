"""test_attention.py — 模型前向与注意力掩码测试。"""

import sys
from pathlib import Path

import torch

# 保证能 import 项目内模块（在项目根运行 pytest）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.gpt import GPT, GPTConfig  # noqa: E402


def test_attention_shape():
    """前向输出形状正确。"""
    cfg = GPTConfig(vocab_size=100, n_embd=32, n_head=4, block_size=64)
    model = GPT(cfg)
    x = torch.randint(0, 100, (2, 64))
    logits, past = model(x)
    assert logits.shape == (2, 64, 100)
    # KV cache 每层返回 (K, V)
    assert len(past) == cfg.n_layer
    assert past[0][0].shape == (2, 4, 64, 8)


def test_attention_is_causal():
    """因果掩码：位置 i 只依赖 0..i。"""
    cfg = GPTConfig(vocab_size=50, n_embd=16, n_head=2, block_size=16, dropout=0.0)
    model = GPT(cfg).eval()

    # 输入 [a, b] 时，第二个位置的 logits 不应受到未来影响。
    # 用同一个 token 序列，分别取位置 0 与位置 1 的输出，验证位置 0 输出一致。
    with torch.no_grad():
        x = torch.randint(0, 50, (1, 2))
        logits_full, _ = model(x)
        logits_0, _ = model(x[:, :1])
        # 位置 0 的 logits 应与只看单 token 时一致（无未来信息）
        assert torch.allclose(logits_full[0, 0], logits_0[0, 0], atol=1e-5)


def test_weight_tied():
    """输入 embedding 与输出头权重绑定。"""
    cfg = GPTConfig(vocab_size=100, n_embd=32, n_head=4)
    model = GPT(cfg)
    assert model.transformer.wte.weight is model.lm_head.weight


def test_num_params():
    """参数量可计算且为正。"""
    cfg = GPTConfig(vocab_size=100, n_embd=32, n_head=4, n_layer=2)
    model = GPT(cfg)
    assert model.num_params() > 0
