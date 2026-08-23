# LLM 推理优化 · 架构说明

> 从零实现的 **decoder-only GPT** 推理优化工具箱，按"一步步逼近真实推理引擎"的四条主线组织。

## 系统分层

```text
模型层  gpt.py                 # decoder-only GPT：KV Cache + prefill/decode 分离
量化层  quantize.py            # INT8 / INT4(group-wise) / FP8 权重量化（weight-only）
采样层  speculative.py         # 投机解码：draft + 并行验证
调度层  continuous.py          # Continuous Batching：多请求动态批调度
服务层  serving.py             # 批量生成服务（batched_generate）
工具    train_utils.py         # 编码 / 训练辅助
```

## 各模块职责

| 模块 | 作用 | 关键点 |
|---|---|---|
| `gpt.py` | 因果自回归 GPT | `CausalSelfAttention` 带 K/V 缓存；`forward` 返回 `(logits, presents)`；`forward_padded` / `forward_continuous` 支持批内不同缓存长度 |
| `quantize.py` | 权重量化对比 | `quantize_weight_tensor(w, bits)`：`32/8/4/"fp8"`，weight-only，反量化回 fp32 度量误差；`make_int8_dynamic` 用 torch 原生动态量化 |
| `speculative.py` | 投机解码 | draft 模型生成候选 token，target 并行验证，接受/拒绝按置信度 |
| `continuous.py` | Continuous Batching | 每步动态确定批内请求，处理不同长度 K/V 缓存，`ContinuousBatchingEngine` |
| `serving.py` | 批量生成 | `batched_generate` 一次服务多个请求 |
| `train_utils.py` | 训练辅助 | `encode` / `train_char_gpt` |

## 优化主线

1. **解码复杂度**：KV Cache + prefill/decode 分离 → 解码 O(T²)→O(T)
2. **权重精度**：INT8 / INT4 / FP8 量化，weight-only，度量还原误差与显存节省
3. **采样算法**：投机解码，target 前向次数大幅下降
4. **服务吞吐**：Continuous Batching，吞吐随 batch 近线性增长

## 基准与报告

- `benchmark.py` → KV Cache 加速比（见 `reports/kv_cache_speedup.png` + `kv_cache_report.md`）
- `quant_compare.py` → 各精度对比（`reports/quant_compare*.{png,md}`）
- `spec_bench.py` → 投机解码（`reports/spec_report.md`）
- `cont_bench.py` → Continuous Batching（`reports/cont_batching.png`）
- `serve_bench.py` → 服务延迟/吞吐（`reports/serving_*.png`）

> 完整定量结论见仓库根目录的 `REPORT.md`（汇总四项优化）。

## 运行基准

```bash
python LLM推理优化/benchmark.py       # KV Cache 加速
python LLM推理优化/quant_compare.py   # 量化对比
python LLM推理优化/spec_bench.py      # 投机解码
python LLM推理优化/cont_bench.py      # Continuous Batching
python LLM推理优化/serve_bench.py     # 服务基准
```

## 测试

```bash
pip install -e "LLM推理优化[dev]"
pytest LLM推理优化/tests   # test_gpt.py / test_quantize.py（正确性 + KV Cache 一致性）
```
