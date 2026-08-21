"""continuous batching 的正确性：动态 slot 复用引擎输出应等于逐条解码。"""

import torch
from llm.continuous import ContinuousBatchingEngine
from llm.gpt import GPT, GPTConfig


def _model(seed=0):
    torch.manual_seed(seed)
    cfg = GPTConfig(vocab_size=40, n_layer=2, n_head=2, n_embd=32, block_size=64)
    return GPT(cfg).eval()


def test_continuous_matches_sequential():
    model = _model()
    engine = ContinuousBatchingEngine(model, max_batch=4)

    # 请求长度参差不齐，触发动态 slot 复用
    prompts = torch.randint(0, 40, (7, 12))
    max_news = [5, 3, 8, 6, 4, 7, 3]

    requests = [(prompts[i : i + 1], max_news[i]) for i in range(7)]
    results = engine.serve(requests)

    assert len(results) == 7
    for i in range(7):
        seq = model.generate(
            prompts[i : i + 1], max_new_tokens=max_news[i], use_kv_cache=True, sample=False
        )
        assert torch.equal(results[i], seq), f"req {i} mismatch"


def test_continuous_batch_never_exceeds_limit():
    model = _model()
    engine = ContinuousBatchingEngine(model, max_batch=2)
    prompts = torch.randint(0, 40, (6, 8))
    requests = [(prompts[i : i + 1], 6) for i in range(6)]
    results = engine.serve(requests)
    for i in range(6):
        assert results[i].size(1) == 6
