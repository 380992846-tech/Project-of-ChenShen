"""GPT KV Cache 的单元测试。

核心断言：KV Cache 生成与非 KV Cache 生成必须**逐 token 完全一致**。
"""

import pytest
import torch
from llm.gpt import GPT, GPTConfig


@pytest.fixture
def model():
    torch.manual_seed(42)
    cfg = GPTConfig(
        vocab_size=64,
        n_layer=2,
        n_head=2,
        n_embd=32,
        block_size=64,
        dropout=0.0,
    )
    return GPT(cfg).eval()


@pytest.fixture
def prompt():
    torch.manual_seed(7)
    return torch.randint(0, 64, (1, 20))


def test_generate_kv_matches_no_kv(model, prompt):
    """KV Cache 与非 KV 的贪心生成结果必须完全一致。"""
    out_kv = model.generate(prompt, max_new_tokens=25, use_kv_cache=True, sample=False)
    out_plain = model.generate(prompt, max_new_tokens=25, use_kv_cache=False, sample=False)
    assert torch.equal(out_kv, out_plain)


def test_kv_cache_logits_match_full_forward(model, prompt):
    """KV 缓存逐步 logits 应与一次性全序列前向完全一致。"""
    # 全序列前向（非 KV），取每个新位置输出的 logits
    full_seq = prompt
    for _ in range(6):
        logits_full, _ = model(full_seq)
        full_seq = torch.cat([full_seq, logits_full[:, -1:].argmax(dim=-1)], dim=1)

    # KV 逐步生成，逐步比对 logits
    past = None
    seq = prompt.clone()
    with torch.no_grad():
        for i in range(6):
            input_ids = seq[:, -1:] if past is not None else seq
            logits_kv, past = model(input_ids, past)
            # 与全序列前向在同一位置的 logits 比对
            full_logits, _ = model(seq)
            assert torch.allclose(logits_kv[:, -1], full_logits[:, -1], atol=1e-5)
            next_tok = logits_kv[:, -1:].argmax(dim=-1)
            seq = torch.cat([seq, next_tok], dim=1)


def test_kv_cache_output_shape(model, prompt):
    """生成的 token 形状应为 (B, max_new_tokens)。"""
    out = model.generate(prompt, max_new_tokens=12, use_kv_cache=True, sample=True, temperature=0.8)
    assert out.shape == (1, 12)


def test_model_learns_simple_sequence():
    """小规模训练冒烟：在简单自回归序列上训练后损失应下降。"""
    torch.manual_seed(0)
    cfg = GPTConfig(vocab_size=32, n_layer=2, n_head=2, n_embd=32, block_size=64)
    m = GPT(cfg)
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3)

    # 构造固定循环序列：token_i = i % 32
    seq = torch.arange(0, 64) % 32
    x = seq[:-1].unsqueeze(0)
    y = seq[1:].unsqueeze(0)

    def loss():
        logits, _ = m(x)
        return torch.nn.functional.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))

    initial = loss().item()
    for _ in range(40):
        opt.zero_grad()
        loss_val = loss()
        loss_val.backward()
        opt.step()
    final = loss().item()
    assert final < initial, f"training loss did not decrease: {initial:.4f} -> {final:.4f}"
