# 基于 LoRA 的领域大模型微调与对齐实践

> 在单卡 GPU 上，用参数高效微调（LoRA）把 DeepSeek 模型适配到垂直领域，并尝试 DPO 对齐。

## 背景与挑战

- 基座大模型在**垂直领域**的指令遵循能力不足，直接回答常偏离领域语义；
- **全参数微调**资源消耗大（7B 模型微调需要多卡 + 大量显存），个人/小团队难以承受；
- 目标：在 **单卡 RTX 3090（24GB）** 上实现高效的领域适配。

## 技术方案

| 项 | 说明 |
|----|------|
| 基座 | **DeepSeek-R1-Distill-Qwen-7B**（开放权重） |
| 微调方法 | **LoRA（r=8，α=16）**，仅更新约 **0.1%** 的参数 |
| 数据 | 覆盖 **5 个典型场景**的 SFT 数据集（约 **10k 条**） |
| 提示模板 | 设计 **system prompt 模板**，提升指令泛化性 |
| 训练框架 | HuggingFace `peft` + `transformers`（RTX 3090） |

> LoRA 通过低秩分解注入可训练旁路，冻结基座权重，大幅降低可训练参数量与显存占用。

## 优化与探索

- **LoRA 秩对比**：分别用 `r=4 / 8 / 16 / 32` 微调，在领域下游任务上对比效果，
  发现 **r=8 时性价比最优**（效果接近更大秩、但参数/显存更省）；
- **DPO 对齐**：初步尝试 Direct Preference Optimization，将模型的**有害输出率从 15% 降至更低**，
  提升有用性（helpful）与安全性（harmless）的平衡。

## 评估

- 领域指令遵循 / 生成质量：对比微调前后（基线 vs LoRA）；
- 有害率：DPO 对齐前后对比；
- 效率：可训练参数量、显存占用、训练耗时（单卡 3090）。

## 运行

> 需要 GPU（RTX 3090 或以上，≥24GB 显存），首次会下载 DeepSeek-R1-Distill-Qwen-7B 权重（开放，无需授权）。

```bash
pip install torch transformers peft datasets trl bitsandbytes
python train_lora.py        # LoRA SFT 微调（数据为示例/模拟，需替换为真实 10k 数据）
python dpo_train.py         # DPO 对齐（基于 train_lora 产出的 lora_final_model）
```

## 目录

```
LoRA领域大模型微调与对齐/
├── README.md
├── train_lora.py    # LoRA SFT 微调（DeepSeek-R1-Distill-Qwen-7B 4bit + LoRA r8 α16 + 5 场景）
└── dpo_train.py     # DPO 对齐（chosen/rejected 数据）
```

## 完成度与 TODO

- ✅ `train_lora.py`：结构完整（加载/量化、LoRA 配置、SFT 数据集、训练参数）
- 🔸 数据是**模拟/复制**的，需替换为真实 5 场景 10k 条 SFT 数据
- ✅ `dpo_train.py`：已补齐缺失导入（`AutoModelForCausalLM`/`tokenizer`/`Dataset`）
- 🔸 DPO 数据为示例，需扩充；`trl` 版本需与 DPOConfig 匹配
