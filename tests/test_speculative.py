"""投机解码的单元测试：多 token 并行验证正确性 + 投机分布精确性。"""

import copy

import torch
from llm.gpt import GPT, GPTConfig
from llm.speculative import speculative_decode


def _model(vocab=40, seed=0, n_layer=2, n_embd=32, block_size=64):
    torch.manual_seed(seed)
    cfg = GPTConfig(
        vocab_size=vocab, n_layer=n_layer, n_head=2, n_embd=n_embd, block_size=block_size
    )
    return GPT(cfg).eval(), cfg


def test_multi_token_decode_matches_full_forward():
    """decode 阶段一次性验证多个新 token 时，logits 应与全序列前向一致。"""
    model, cfg = _model(block_size=64)
    prompt = torch.randint(0, cfg.vocab_size, (1, 16))
    # 先 prefill
    _, past = model(prompt, None)
    # 一次性解码 3 个新 token
    new_tokens = torch.randint(0, cfg.vocab_size, (1, 3))
    logits_blk, _ = model(new_tokens, past)
    # 全序列前向对照
    full = torch.cat([prompt, new_tokens], dim=1)
    logits_full, _ = model(full)
    assert torch.allclose(logits_blk[:, 0], logits_full[:, 16], atol=1e-5)
    assert torch.allclose(logits_blk[:, 2], logits_full[:, 18], atol=1e-5)


def test_spec_greedy_with_identical_draft_matches_target():
    """draft == target 时，贪心投机解码应等于 target 直接贪心解码。"""
    model, cfg = _model()
    draft = copy.deepcopy(model)
    prompt = torch.randint(0, cfg.vocab_size, (1, 8))
    torch.manual_seed(0)
    target_out = model.generate(prompt, max_new_tokens=20, use_kv_cache=True, sample=False)
    torch.manual_seed(0)
    spec_out = speculative_decode(draft, model, prompt, gamma=4, max_new_tokens=20, sample=False)
    assert torch.equal(spec_out, target_out)


def test_spec_distribution_matches_target():
    """投机采样的首 token 经验分布应与 target 分布一致（精确性）。"""
    model, cfg = _model(vocab=20, n_layer=1, n_embd=16, block_size=64)
    draft = copy.deepcopy(model)
    prompt = torch.randint(0, cfg.vocab_size, (1, 8))

    # target 给定上下文后第一个新 token 的分布
    with torch.no_grad():
        logits, _ = model(prompt)
    p = torch.softmax(logits[:, -1, :], dim=-1)[0].cpu().numpy()

    n = 1500
    counts = {}
    for _ in range(n):
        tok = speculative_decode(draft, model, prompt, gamma=3, max_new_tokens=1, sample=True)
        v = tok[0, 0].item()
        counts[v] = counts.get(v, 0) + 1

    empirical = torch.zeros(cfg.vocab_size)
    for v, c in counts.items():
        empirical[v] = c / n
    tv = 0.5 * torch.abs(empirical - torch.tensor(p)).sum().item()
    assert tv < 0.1, f"total variation {tv:.3f} too large"
