"""批量解码的正确性测试：batch 输出应等于逐条单独解码。"""

import torch
from llm.gpt import GPT, GPTConfig
from llm.serving import batched_generate


def test_batched_matches_individual():
    torch.manual_seed(0)
    cfg = GPTConfig(vocab_size=40, n_layer=2, n_head=2, n_embd=32, block_size=64)
    model = GPT(cfg).eval()

    prompts = torch.randint(0, 40, (4, 16))

    batch_out = batched_generate(model, prompts, gen_len=12, sample=False)

    for i in range(4):
        single = batched_generate(model, prompts[i : i + 1], gen_len=12, sample=False)
        assert torch.equal(batch_out[i : i + 1], single), f"batch row {i} mismatch"


def test_batched_shape():
    torch.manual_seed(1)
    cfg = GPTConfig(vocab_size=40, n_layer=1, n_head=2, n_embd=32, block_size=64)
    model = GPT(cfg).eval()
    prompts = torch.randint(0, 40, (6, 12))
    out = batched_generate(model, prompts, gen_len=20, sample=False)
    assert out.shape == (6, 20)
