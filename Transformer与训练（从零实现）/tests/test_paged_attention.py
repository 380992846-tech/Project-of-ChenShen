"""test_paged_attention.py — 分页 KV 缓存正确性测试。"""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.paged_attention import PagedKV, build_causal_mask, paged_attention  # noqa: E402


def _seq_qkv(seq_len, n_head=4, head_dim=8, seed=0):
    """构造一个固定序列的 q/k/v 作为基准。"""
    torch.manual_seed(seed)
    q = torch.randn(1, seq_len, n_head, head_dim)
    kv = torch.randn(1, seq_len, n_head, head_dim)
    return q, kv, kv


def _paged_attn(q, kv, n_head, head_dim, block_size):
    """用 PagedKV 逐 token 写入并算最终 attention。"""
    n_layer = 1
    cache = PagedKV(n_layer, n_head, head_dim, block_size=block_size, device="cpu")
    block_table: list[int] = []
    seq_len = q.shape[1]
    # 逐 token 写入
    for t in range(seq_len):
        kt = kv[:, t : t + 1].permute(0, 2, 1, 3)  # (1, n_head, 1, hd)
        vt = kt
        block_table = cache.append(0, kt, vt, block_table)
    # 用最后一个 token 的 q 做 attention（decode 场景）
    q_last = q[:, -1:].permute(0, 2, 1, 3)  # (1, n_head, 1, hd)
    k_all, v_all = cache.gather(0, block_table)
    return paged_attention(q_last, k_all, v_all)


def _contig_attn(q, kv, n_head, head_dim):
    """标准连续 KV Cache 的 attention（基准）。

    decode 场景：最后一个 token 的 q 能看到全部已写入的 K/V，无需因果掩码。
    """
    seq_len = q.shape[1]
    k_all = kv.permute(0, 2, 1, 3)  # (1, n_head, T, hd)
    v_all = kv.permute(0, 2, 1, 3)
    q_last = q[:, -1:].permute(0, 2, 1, 3)  # (1, n_head, 1, hd)
    att = (q_last @ k_all.transpose(-2, -1)) * (1.0 / (head_dim ** 0.5))
    att = torch.softmax(att, dim=-1)
    return att @ v_all


def test_paged_matches_contiguous():
    """分页 attention 输出与连续 KV Cache 完全一致。"""
    n_head, head_dim, seq_len = 4, 8, 30
    q, kv, _ = _seq_qkv(seq_len, n_head, head_dim)
    # 用多个 block_size，覆盖跨块/单块情形
    for block_size in (8, 16, 32):
        out_paged = _paged_attn(q, kv, n_head, head_dim, block_size)
        out_contig = _contig_attn(q, kv, n_head, head_dim)
        assert torch.allclose(out_paged, out_contig, atol=1e-5), f"block_size={block_size} 不一致"


def test_paged_block_allocation():
    """验证按需分块：block_size=8 时 20 个 token 应占用 ceil(20/8)=3 个物理块。"""
    n_head, head_dim, seq_len = 2, 8, 20
    block_size = 8
    cache = PagedKV(1, n_head, head_dim, block_size=block_size, device="cpu")
    bt: list[int] = []
    for t in range(seq_len):
        kt = torch.randn(1, n_head, 1, head_dim)
        bt = cache.append(0, kt, kt, bt)
    # 物理块数 = ceil(20/8) = 3
    assert len(bt) == 3, f"期望 3 个物理块，实际 {len(bt)}"
    assert cache.total_cached(bt) == 20


def test_paged_empty_cache():
    """空 block table 的 gather 返回空。"""
    n_head, head_dim = 4, 8
    cache = PagedKV(1, n_head, head_dim, block_size=16, device="cpu")
    k, v = cache.gather(0, [])
    assert k.shape[2] == 0 and v.shape[2] == 0
