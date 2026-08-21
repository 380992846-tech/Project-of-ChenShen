# continuous batching 基准

- 模型参数：`187,328`；请求 `64`，prompt `16`，长度均匀分布在 `[2,30]`
- 有效 token 总数：`1038`

| 调度方式 | 墙钟 (s) | 有效吞吐 (tokens/s) |
|---------|----------|---------------------|
| sequential | 3.031 | 342 |
| static batch | 0.517 | 2008 |
| **continuous batching** | 0.817 | **1271** |

## 结论
- **continuous batching 远超串行**（~4×），且正确实现了动态 slot 复用（输出与逐条解码完全一致，测试覆盖）；
- 本 CPU 玩具基准里 static 略胜 continuous，是因为小模型+短序列下 static 的紧凑缓存没有 padding/克隆开销，尾部浪费也小；
- continuous 的真正优势在 **GPU + 长序列 + 长度高差异 + 稳定请求流 + PagedAttention 式高效显存分配** 场景下才会完全释放（本实现用朴素 padded 缓存演示 slot 复用语义）。

> 说明：本实现重点在**正确性**（slot 复用语义）与相对串行的收益；要榨出相对 static 的优势，需配合 PagedAttention 的按块分配（见 README Roadmap）。
