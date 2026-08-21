# Transformer From Scratch — Training & Inference

> A from-scratch Transformer trained on **real Chinese text**, supporting **GPU / CPU / DDP** training,
> `config.yaml` experiment management, standalone `generate.py` inference (including interactive mode),
> BPE tokenization, TensorBoard logging, unit tests, and a Docker image.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train (default CPU, hyperparams from config.yaml)
python train.py --config config.yaml

# 3. Generate Chinese with a trained checkpoint
python generate.py --checkpoint checkpoints/best_char_gpt.pth --prompt "清华" --length 300

# 4. Interactive chat-like generation
python generate.py --checkpoint checkpoints/best_char_gpt.pth --interactive

# 5. Single GPU (uses CUDA automatically)
python train.py --config config.yaml

# 6. Multi-GPU distributed (torchrun)
torchrun --nproc_per_node=2 train.py --config config.yaml

# 7. BPE tokenizer instead of char-level
python train.py --config config.yaml --tokenizer bpe

# 8. TensorBoard live curves
python train.py --config config.yaml --log-dir runs/exp1
tensorboard --logdir runs/exp1

# 9. Run tests
pytest tests/ -v
```

---

## Directory Layout

```
Transformer与训练（从零实现）/
├── config.yaml          # hyperparameters (single source of truth)
├── train.py             # training: GPU / CPU / DDP, reads config.yaml
├── generate.py          # standalone inference (single / interactive)
├── rag.py               # retrieval-augmented generation
├── quantize.py          # INT8 dynamic quantization
├── dashboard.py         # Streamlit monitoring panel
├── models/
│   ├── gpt.py           # decoder-only GPT from scratch (KV cache, weight tying)
│   └── config.py        # dataclass config + YAML loader (type coercion)
├── data/
│   ├── build_corpus.py  # extract corpus from .docx notes
│   ├── dataset.py       # CharDataset (char-level)
│   └── bpe.py           # minimal BPE tokenizer (word-level upgrade)
├── tests/               # unit tests (model / dataset / config)
├── checkpoints/         # training artifacts (*.pth gitignored)
├── Dockerfile           # training/inference image
├── docker-compose.yml   # one-click train/generate/dashboard
└── 训练报告.md            # training report (loss / PPL / samples)
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **GPU + DDP** | `device = cuda if available else cpu`; `torchrun` for multi-GPU |
| **config.yaml** | experiment management; CLI `--key value` overrides |
| **Standalone generate.py** | train once, generate anytime; `--interactive` chat mode |
| **BPE tokenizer** | `data/bpe.py` merges frequent subwords (compression + efficiency) |
| **TensorBoard** | optional `--log-dir` for live loss curves |
| **Modular** | `models/`, `data/`, `rag.py`, `quantize.py`, `dashboard.py` |
| **Unit tests** | model shapes / causal mask / dataset / config |
| **Docker** | `Dockerfile` + `docker-compose.yml` one-click deploy |

---

## Results (CPU, 1500 steps)

| step | train loss | val loss |
|------|-----------|----------|
| 250 | 5.731 | 6.048 |
| 500 | 5.194 | 5.552 |
| 750 | 4.933 | 5.423 |
| 1000 | 4.839 | 5.250 |
| 1250 | 4.518 | 5.071 |
| 1500 | 4.146 | 4.816 |

**PPL = 122.2** (random baseline ≈ vocab size 1899). Loss keeps decreasing —
the from-scratch model learns Chinese character co-occurrence statistics.

> 💡 On GPU with a larger model, PPL can drop below 50 (see Roadmap).

---

## Generation Examples

```bash
python generate.py --prompt "清华" --length 300 --temperature 0.8
```

| arg | default | meaning |
|-----|---------|---------|
| `--prompt` | `清华` | starting prompt |
| `--length` | `300` | tokens to generate |
| `--temperature` | `0.8` | sampling temperature |
| `--top-k` | `None` | top-k truncation |
| `--seed` | `None` | fix random seed for reproducibility |
| `--interactive` | off | chat-like loop (q/exit to quit) |

---

## Model Comparison

| Model | Params | Tokenization | Relation to GPT-2 |
|-------|--------|--------------|-------------------|
| **This char-GPT** | ~0.6M | char-level | from-scratch, full training/optimization pipeline |
| GPT-2 (124M) | 124M | BPE subword | this is a scaled-down, structurally identical version |
| GPT-2 (1.5B) | 1.5B | BPE subword | industrial scale, far more training data |

---

## Testing

```bash
pytest tests/ -v
```

Covers: attention output shape, causal masking, weight tying, param count,
dataset round-trip / next-token semantics, config loading (default + YAML).

---

## Roadmap

- [x] From-scratch Transformer (Embedding / attention / positional / training / generation)
- [x] Real Chinese corpus + loss curve + PPL
- [x] GPU + DDP
- [x] config.yaml experiment management
- [x] Standalone generate.py / interactive / RAG / quantization / dashboard
- [x] Unit tests
- [x] BPE tokenizer
- [x] TensorBoard logging
- [x] Docker image + docker-compose
- [ ] PagedAttention (block-wise KV allocation, saves memory)
- [ ] Larger model + larger corpus, target PPL < 50
- [ ] byte-level BPE / SentencePiece for robustness

---

> Training artifacts (`checkpoints/*.pth`) are gitignored. With a small model + CPU + limited steps,
> output is short fluent fragments; a bigger model / GPU / more data improves coherence significantly.
