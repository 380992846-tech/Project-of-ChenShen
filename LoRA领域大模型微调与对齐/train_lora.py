import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import os

# ==================== 0. 全局配置 ====================
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
MAX_LEN = 1024            # prompt + 回复 的最大长度（调大一点，避免回复被截掉导致 loss 全被 mask）
DATA_SIZE = 10_000
EVAL_RATIO = 0.05
OUTPUT_DIR = "./lora_checkpoints"
FINAL_DIR = "./lora_final_model"

# ==================== 1. 加载基座模型 ====================
# 4bit 量化加载（3090 24G 友好）
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)
model.config.use_cache = False          # 训练时关闭 KV cache，配合梯度检查点再省显存
model = prepare_model_for_kbit_training(model)

# ==================== 2. 配置 LoRA ====================
lora_config = LoraConfig(
    r=8,                     # 秩
    lora_alpha=16,           # 缩放系数
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # ~0.1% 参数可训练

# ==================== 3. 构造数据集（示例，替换为真实 10k 数据） ====================
SYSTEM_TEMPLATES = {
    "law": "你是一位专业的法律顾问，请基于中国法律法规给出准确、严谨的回答。",
    "finance": "你是一位金融分析师，请提供客观、数据驱动的金融信息。",
    "code": "你是一位资深软件工程师，请编写高质量、可运行的代码。",
    "medical": "你是一位医疗健康顾问，请提供科学的健康建议，不替代医生诊断。",
    "general": "你是一位乐于助人的AI助手，请提供清晰、有用的回答。",
}

INSTRUCTIONS = [
    "什么是合同法中的不可抗力条款？",
    "请用Python实现快速排序算法。",
    "感冒和流感的区别是什么？",
    "如何评估一只股票的投资价值？",
    "请解释量子计算的基本原理。",
]

RESPONSES = [
    "不可抗力是指不能预见、不能避免且不能克服的客观情况...",
    "```python\ndef quicksort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)\n```",
    "感冒和流感均由病毒引起，但症状严重程度不同...",
    "评估股票价值可以使用市盈率(PE)、市净率(PB)等指标...",
    "量子计算利用量子叠加和量子纠缠进行计算...",
]


def build_dataset():
    """生成 10k 条示例数据。真实训练时请用 load_dataset() 从 json/parquet 读入。"""
    scenes = list(SYSTEM_TEMPLATES.keys())
    rows = []
    for i in range(DATA_SIZE):
        scene = scenes[i % len(scenes)]
        idx = i % len(INSTRUCTIONS)
        rows.append({
            "system": SYSTEM_TEMPLATES[scene],
            "instruction": INSTRUCTIONS[idx],
            "output": RESPONSES[idx],
        })
    return Dataset.from_list(rows)


dataset = build_dataset()


def format_chat_sample(sample):
    """返回完整目标文本 + 仅 prompt 文本，用于后续 mask prompt 的 loss。"""
    full_messages = [
        {"role": "system", "content": sample["system"]},
        {"role": "user", "content": sample["instruction"]},
        {"role": "assistant", "content": sample["output"]},
    ]
    prompt_messages = full_messages[:-1]  # system + user
    full_text = tokenizer.apply_chat_template(full_messages, tokenize=False, add_generation_prompt=False)
    prompt_text = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
    return {"full_text": full_text, "prompt_text": prompt_text}


dataset = dataset.map(format_chat_sample, remove_columns=dataset.column_names)


def tokenize_fn(sample):
    full = tokenizer(sample["full_text"], truncation=True, max_length=MAX_LEN, padding=False)
    prompt_ids = tokenizer(sample["prompt_text"], truncation=True, max_length=MAX_LEN, padding=False)["input_ids"]
    labels = full["input_ids"].copy()
    # mask prompt（system + user + 助手头部），只对“助手回复”算 loss
    mask_len = min(len(prompt_ids), len(labels))
    labels[:mask_len] = [-100] * mask_len
    return {
        "input_ids": full["input_ids"],
        "attention_mask": full["attention_mask"],
        "labels": labels,
    }


tokenized = dataset.map(tokenize_fn, remove_columns=dataset.column_names, batched=False)

# 拆分训练 / 验证集（供 eval 与 load_best_model_at_end 使用）
split = tokenized.train_test_split(test_size=EVAL_RATIO, seed=42)
train_dataset = split["train"]
eval_dataset = split["test"]

# ==================== 4. 训练配置 ====================
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,      # 有效 batch = 4*4 = 16
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    evaluation_strategy="steps",
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    bf16=True,                          # 与 bf16 计算精度保持一致（原 fp16 与 bf16 混用有隐患）
    gradient_checkpointing=True,        # 7B 在 24G 上必开，否则易 OOM
    report_to="none",
    dataloader_num_workers=4,
    optim="paged_adamw_8bit",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,          # 补上验证集
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, padding=True, label_pad_token_id=-100),
)

# ==================== 5. 训练与保存 ====================
if __name__ == "__main__":
    trainer.train()
    model.save_pretrained(FINAL_DIR)
    tokenizer.save_pretrained(FINAL_DIR)
    print(f"LoRA adapter saved to {FINAL_DIR}")

    # 可选：合并权重成完整模型（对 4bit 基座请先反量化，建议在 bf16 下 merge）
    # from peft import PeftModel
    # merged = model.merge_and_unload()
    # merged.save_pretrained("./merged_model")
