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

## 优化与探索（进行中 / 待验证）

> ⚠️ 以下为**计划或初步方向**，尚未在真实数据上验证，**不要当作已实现的效果**。

- **LoRA 秩对比**（计划）：分别用 `r=4 / 8 / 16 / 32` 微调后在领域下游任务上对比，
  **预期** r=8 性价比最优（效果接近更大秩、但参数/显存更省）——需实测确认；
- **DPO 对齐**（进行中）：目标是降低有害输出、均衡 helpful 与 harmless；
  当前提到的"有害率降低"是**预期目标**，尚未用真实数据量化。

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
├── train_lora.py        # LoRA SFT 微调（已修复：loss 只对回复算、补 eval、开梯度检查点、bf16）
├── dpo_train.py         # DPO 对齐（已修复：参考策略、chat 模板、成对数据、新 DPOConfig）
├── 数据接入说明.md        # 真实数据格式与替换方法
├── _原文备份/            # 原始未修改脚本（便于对拍）
└── data/                # 放 sft.jsonl / dpo.jsonl（自行创建）
```

## 完成度与 TODO

- ✅ `train_lora.py`：结构完整，且已修复：只对助手回复算 loss、补 `eval_dataset`、
  开 `gradient_checkpointing`、精度统一 `bf16`、`max_length` 调大；
- ✅ `dpo_train.py`：补齐导入，且已修复：构造真实 chosen/rejected 对、走 chat 模板、
  用 `create_reference_model` 生成参考策略、对齐新版 `DPOConfig`；
- 🔸 **数据仍是模拟/占位**：SFT 需替换为真实 5 场景 10k 条（`data/sft.jsonl`）；
  DPO 需替换为真实成对偏好数据（`data/dpo.jsonl`），见 `数据接入说明.md`；
- 🔸 `trl` 版本需匹配新的 `DPOConfig/DPOTrainer` API（升级：`pip install -U trl`）；
- 🔸 LoRA 秩对比、DPO 有害率等结论为**待验证目标**，需跑真实数据后确认。

## 修复记录（2026-08-23）

- 修正 `train_lora.py`：改用 `apply_chat_template` 拆分 prompt 并 mask `-100`，只对回复算 loss；
  拆出验证集并传给 `Trainer`；开启 `gradient_checkpointing` 与 `use_cache=False`；
  精度统一为 `bf16`；修正"LLaMA 2 模板"注释；`DataCollatorForSeq2Seq` 指定 `label_pad_token_id=-100`。
- 修正 `dpo_train.py`：DPO 示例数据扩到 4 对；prompt 用 chat 模板格式化；
  用 `create_reference_model` 生成冻结参考策略；补齐 `DPOConfig` 字段与 trl 版本提示。
- 原始未改脚本保留在 `_原文备份/`。
