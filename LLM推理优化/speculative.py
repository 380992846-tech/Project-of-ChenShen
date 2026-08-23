"""
speculative.py
==============

投机解码（Speculative Decoding）——推理优化 Step 3。

原理
----
用小而快的 **draft 模型** 一次性自回归地猜出 ``gamma`` 个候选 token，
再用 **target 模型** 对这些候选做**一次并行前向验证**（配合 KV Cache），
通过拒绝采样（rejection sampling）决定接受哪些。

正确性
------
标准的投机解码在每次被拒绝处按 ``max(0, p - q)`` 重新采样，
从而**精确保持 target 模型的分布**——即投机解码与 target 直接采样
在分布上完全等价，但每次 target 前向能"免费"多产出若干 token，
从而提升吞吐。

参考：Chen et al., "Accelerating Large Language Model Decoding with
Speculative Sampling" (2023)。
"""

from __future__ import annotations

import torch
import torch.nn.functional as F

from gpt import GPT


@torch.no_grad()
def _truncate_past(past, keep_tokens: int):
    """把每层 KV 缓存截断到只保留前 keep_tokens 个时间步。"""
    return [(k[:, :, :keep_tokens, :], v[:, :, :keep_tokens, :]) for k, v in past]


def speculative_decode(
    draft: GPT,
    target: GPT,
    prompt: torch.Tensor,
    gamma: int = 4,
    max_new_tokens: int = 100,
    temperature: float = 1.0,
    sample: bool = True,
    seed: int | None = None,
    return_stats: bool = False,
):
    """
    投机解码生成。

    Args:
        draft: 小而快的草稿模型（与 target 词汇表一致）。
        target: 验证/目标模型。
        prompt: (1, T) 初始 token。
        gamma: 每轮草稿猜测的候选数。
        max_new_tokens: 要生成的新 token 总数。
        sample: True 用精确拒绝采样；False 用贪心（argmax 匹配才接受）。
        seed: 固定随机种子（用于确定性测试）。
        return_stats: True 时额外返回统计 dict
            (``avg_tokens_per_verification`` / ``n_verifications``)。
    Returns:
        (1, max_new_tokens) 生成的 token；若 return_stats，返回 (tokens, stats)。
    """
    if seed is not None:
        torch.manual_seed(seed)
    draft.eval()
    target.eval()

    seq = prompt.clone()
    out: list[torch.Tensor] = []
    total = 0
    n_verifications = 0
    total_committed = 0

    # target 先 prefill prompt，并记下最后一个位置 logits（用于判定候选 token 0）
    prefill_logits, t_past = target(seq, None)
    t_seq_len = seq.size(1)
    p0 = F.softmax(prefill_logits[:, -1, :] / temperature, dim=-1)  # 候选 0 的分布

    while total < max_new_tokens:
        n_verifications += 1
        # ---- 1) draft 自回归生成 gamma 个候选 ----
        candidates: list[torch.Tensor] = []
        d_probs: list[torch.Tensor] = []
        d_past = None
        d_seq = seq
        for _ in range(gamma):
            input_ids = d_seq[:, -1:] if d_past is not None else d_seq
            d_logits, d_past = draft(input_ids, d_past)
            d_logits = d_logits[:, -1, :] / temperature
            q = F.softmax(d_logits, dim=-1)
            tok = torch.multinomial(q, 1) if sample else q.argmax(dim=-1, keepdim=True)
            candidates.append(tok)
            d_probs.append(q)
            d_seq = torch.cat([d_seq, tok], dim=1)

        # ---- 2) target 一次并行验证 gamma 个候选 ----
        # 注意：forward 对候选 i 的输出 logits[i] 预测的是候选 i 之后的一个 token，
        # 即它是**候选 i+1** 的分布。因此：
        #   候选 0 的分布 = p0（prefill 最后一位）
        #   候选 i (i>=1) 的分布 = fwd_logits[i-1]
        #   全部接受后的额外 token 分布 = fwd_logits[gamma-1]
        cand = torch.cat(candidates, dim=1)  # (1, gamma)
        fwd_logits, t_new_past = target(cand, t_past)  # (1, gamma, vocab)
        p_fwd = F.softmax(fwd_logits / temperature, dim=-1)

        # ---- 3) 拒绝采样决定接受哪些 ----
        accepted: list[torch.Tensor] = []
        for i in range(gamma):
            t_i = candidates[i]
            p_i = p0 if i == 0 else p_fwd[:, i - 1, :]
            q_i = d_probs[i]
            p_t = p_i[0, t_i[0, 0].item()].item()
            q_t = q_i[0, t_i[0, 0].item()].item()
            accept_prob = min(1.0, p_t / (q_t + 1e-12))
            if (not sample) or (torch.rand(1).item() < accept_prob):
                accepted.append(t_i)
            else:
                # 从 max(0, p_i - q_i) 归一化分布重新采样（保证分布精确性）
                adj = torch.clamp(p_i[0] - q_i[0], min=0.0)
                if adj.sum() <= 0.0:
                    adj = p_i[0]
                adj = adj / adj.sum()
                accepted.append(torch.multinomial(adj, 1))
                break

        # 全部接受时，多采样一个 token（来自 target 分布）
        if len(accepted) == gamma:
            extra_dist = p_fwd[:, gamma - 1, :]
            if sample:
                extra = torch.multinomial(extra_dist, 1)
            else:
                extra = extra_dist.argmax(dim=-1, keepdim=True)
            accepted.append(extra)

        committed = torch.cat(accepted, dim=1)  # (1, n_new)
        n_new = committed.size(1)
        seq = torch.cat([seq, committed], dim=1)
        out.append(committed)
        total += n_new
        total_committed += n_new

        # ---- 4) 同步 target KV 缓存到已接受的长度 ----
        if len(accepted) == gamma + 1:
            # 全部接受 + 额外 token：其 KV 尚未计算，补一步 target 前向
            _, t_past = target(accepted[-1], t_new_past)
        else:
            t_past = _truncate_past(t_new_past, t_seq_len + n_new)
        t_seq_len += n_new

    tokens = torch.cat(out, dim=1)[:, :max_new_tokens]
    if return_stats:
        stats = {
            "avg_tokens_per_verification": total_committed / max(n_verifications, 1),
            "n_verifications": n_verifications,
        }
        return tokens, stats
    return tokens
