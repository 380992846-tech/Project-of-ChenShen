"""GPT 前向与 KV Cache 正确性测试。"""

import torch

from gpt import GPT, GPTConfig


def test_config_defaults():
    c = GPTConfig()
    assert c.vocab_size == 256
    assert c.n_layer == 4
    assert c.n_head == 4
    assert c.n_embd == 128


def test_forward_shape_and_presents():
    cfg = GPTConfig(vocab_size=128, n_layer=2, n_head=4, n_embd=64, block_size=64)
    m = GPT(cfg)
    x = torch.randint(0, 128, (2, 16))
    logits, presents = m(x)
    assert logits.shape == (2, 16, 128)
    assert len(presents) == cfg.n_layer


def test_generate_kv_cache_matches_plain():
    cfg = GPTConfig(vocab_size=128, n_layer=2, n_head=4, n_embd=64, block_size=64)
    m = GPT(cfg)
    prompt = torch.randint(0, 128, (1, 8))

    torch.manual_seed(0)
    out_kv = m.generate(prompt, max_new_tokens=4, use_kv_cache=True, sample=False)

    torch.manual_seed(0)
    out_plain = m.generate(prompt, max_new_tokens=4, use_kv_cache=False, sample=False)

    # 是否开 KV Cache 都应得到相同、可复现的输出序列（generate 返回新生成的 token）
    assert out_kv.shape == (1, 4)
    assert torch.equal(out_kv, out_plain)
