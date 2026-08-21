"""models/paged_attention.py — 分页 KV 缓存（PagedAttention）

vLLM 的核心思想：KV 缓存按固定大小的 **block** 分块存储，用 **block table**
把每个请求的逻辑块映射到物理块。只有在需要时才分配物理块，而不是预留
``max_length`` 的连续内存——这能显著节省显存并减少碎片。

与 `gpt.py` 里"整段连续拼接"的 KV Cache 相比，本模块实现了：
- **按需分块**：token 达到 block_size 才申请下一个物理块；
- **逻辑块 -> 物理块**的映射表（block table），支持请求间共享缓存的基础；
- **分页 attention**：通过 gather 把本请求相关的物理块 K/V 取出计算注意力。

教学说明：这是简化版——固定为单请求逐 token 解码（B=1），
不实现 vLLM 的跨请求块共享与 copy-on-write，但完整保留了"分页 + 按需分配 +
block table 寻址"三个核心语义，可作为理解 PagedAttention 的起点。

用法::

    from models.paged_attention import PagedKV, paged_attention

    cache = PagedKV(n_layer=4, n_head=4, head_dim=32, block_size=16, device='cpu')
    # 每层写入新 token 的 K/V，并返回该层输出
    # 见下方 ``paged_attention`` 示例
"""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F

BlockTable = list[int]  # 逻辑块索引 -> 物理块索引


class PagedKV:
    """分页 KV 缓存。

    每个请求持有一张 block table。物理块池按需分配，block_size 个位置一组。
    """

    def __init__(self, n_layer: int, n_head: int, head_dim: int,
                 block_size: int = 16, device="cpu", max_blocks: int = 1024):
        self.n_layer = n_layer
        self.n_head = n_head
        self.head_dim = head_dim
        self.block_size = block_size
        self.device = device
        self.max_blocks = max_blocks

        # 物理块池：K/V 各 (max_blocks, block_size, n_head, head_dim)
        # 预分配池（内存大小 = max_blocks * block_size，但逻辑上按需使用）
        shape = (max_blocks, block_size, n_head, head_dim)
        self.k_pool = torch.zeros(shape, dtype=torch.float32, device=device)
        self.v_pool = torch.zeros(shape, dtype=torch.float32, device=device)
        # 每个物理块已被占用的位置数（0 表示空闲块，或已写入长度）
        self.used = torch.zeros(max_blocks, dtype=torch.long, device=device)

    # ------------------------------------------------------------ 块分配
    def alloc_block(self) -> int:
        """分配一个空闲物理块，返回其索引；无空闲则 -1。"""
        free = torch.nonzero(self.used == 0, as_tuple=False)
        if free.numel() == 0:
            raise RuntimeError("PagedKV: 物理块池耗尽，增大 max_blocks")
        idx = int(free[0].item())
        self.used[idx] = 0  # 标记为已分配但空
        return idx

    def free_block(self, idx: int) -> None:
        self.used[idx] = 0

    # ------------------------------------------------------------ 写入
    def append(self, layer: int, k: torch.Tensor, v: torch.Tensor,
               block_table: BlockTable) -> BlockTable:
        """把新 token 的 K/V 写入指定层的分页缓存。

        Args:
            layer: 层索引。
            k, v: (1, 1, n_head, head_dim) 单个 token。
            block_table: 该请求当前 block table（逻辑块 -> 物理块）。

        Returns:
            更新后的 block table（若申请了新物理块会增长）。
        """
        log_tok = sum(self.used[bidx].item() for bidx in block_table)  # 已缓存 token 数
        block_idx = log_tok // self.block_size  # 该 token 应落在哪个逻辑块
        pos_in_block = log_tok % self.block_size

        if block_idx >= len(block_table):
            # 需要新物理块
            new_phys = self.alloc_block()
            block_table.append(new_phys)

        phys = block_table[block_idx]
        # 写入 K/V（k/v 形如 (1, n_head, 1, head_dim)，取所有头的该位置）
        self.k_pool[phys, pos_in_block] = k[0, :, 0]
        self.v_pool[phys, pos_in_block] = v[0, :, 0]
        self.used[phys] = min(self.used[phys].item() + 1, self.block_size)
        return block_table

    # ------------------------------------------------------------ 读取
    def gather(self, layer: int, block_table: BlockTable) -> tuple[torch.Tensor, torch.Tensor]:
        """把该请求的所有物理块 K/V 拼成连续视图 (1, n_head, T, head_dim)。"""
        if not block_table:
            return (torch.zeros(1, self.n_head, 0, self.head_dim, device=self.device),
                    torch.zeros(1, self.n_head, 0, self.head_dim, device=self.device))
        ks = [self.k_pool[b, : self.used[b].item()] for b in block_table]
        vs = [self.v_pool[b, : self.used[b].item()] for b in block_table]
        k = torch.cat(ks, dim=0).unsqueeze(0).transpose(1, 2)  # (1, n_head, T, hd)
        v = torch.cat(vs, dim=0).unsqueeze(0).transpose(1, 2)
        return k, v

    def total_cached(self, block_table: BlockTable) -> int:
        return sum(self.used[b].item() for b in block_table)


def paged_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor,
                    mask: torch.Tensor | None = None):
    """分页 attention（等价于标准 scaled dot-product，但 K/V 来自分页 gather）。

    Args:
        q: (B, n_head, T, head_dim) 查询。
        k, v: (B, n_head, T, head_dim) 分页 gather 结果。
        mask: 可选 (1, 1, T, T) 因果掩码。
    """
    B, H, T, hd = q.shape
    T_k = k.shape[2]
    att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(hd))
    if mask is not None:
        att = att.masked_fill(mask[:, :, :T, :T_k] == 0, float("-inf"))
    att = F.softmax(att, dim=-1)
    return att @ v  # (B, n_head, T, head_dim)


def build_causal_mask(T, device="cpu"):
    """(1,1,T,T) 因果下三角掩码。"""
    return torch.tril(torch.ones(1, 1, T, T, device=device))
