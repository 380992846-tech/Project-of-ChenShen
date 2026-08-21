import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset, load_dataset
import json
import os

# ==================== 1. 加载基座模型 ====================
# 使用 DeepSeek 开放权重模型（无需 HF 授权，单卡 3090 用 4bit + LoRA 可训）
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"  # 如果本地没有会自动下载
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 4bit量化加载（3090 24G显存友好）
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = prepare_model_for_kbit_training(model)

# ==================== 2. 配置LoRA ====================
lora_config = LoraConfig(
    r=8,                     # 秩
    lora_alpha=16,           # 缩放系数
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # 应该显示 ~0.1% 参数可训练

# ==================== 3. 构造SFT数据集 ====================
# 这里用示例数据，实际替换成你的10k条数据
def build_dataset():
    # 5个场景的system prompt模板
    system_templates = {
        "law": "你是一位专业的法律顾问，请基于中国法律法规给出准确、严谨的回答。",
        "finance": "你是一位金融分析师，请提供客观、数据驱动的金融信息。",
        "code": "你是一位资深软件工程师，请编写高质量、可运行的代码。",
        "medical": "你是一位医疗健康顾问，请提供科学的健康建议，不替代医生诊断。",
        "general": "你是一位乐于助人的AI助手，请提供清晰、有用的回答。"
    }
    
    # 模拟数据（实际从json/parquet读）
    sample_data = []
    scenes = ["law", "finance", "code", "medical", "general"]
    instructions = [
        "什么是合同法中的不可抗力条款？",
        "请用Python实现快速排序算法。",
        "感冒和流感的区别是什么？",
        "如何评估一只股票的投资价值？",
        "请解释量子计算的基本原理。"
    ]
    responses = [
        "不可抗力是指不能预见、不能避免且不能克服的客观情况...",
        "```python\ndef quicksort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)\n```",
        "感冒和流感均由病毒引起，但症状严重程度不同...",
        "评估股票价值可以使用市盈率(PE)、市净率(PB)等指标...",
        "量子计算利用量子叠加和量子纠缠进行计算..."
    ]
    
    for i in range(len(instructions)):
        scene = scenes[i % len(scenes)]
        sample_data.append({
            "system": system_templates[scene],
            "instruction": instructions[i % len(instructions)],
            "output": responses[i % len(responses)]
        })
    
    # 扩充到10k条（实际使用时读真实数据）
    # 这里用复制模拟，你替换成真正的数据加载
    for i in range(10000):
        idx = i % len(sample_data)
        sample_data.append(sample_data[idx])
    
    return Dataset.from_list(sample_data[:10000])

dataset = build_dataset()

# ==================== 4. 数据预处理 ====================
def format_chat_template(sample):
    # 构造LLaMA 2的对话格式
    messages = [
        {"role": "system", "content": sample["system"]},
        {"role": "user", "content": sample["instruction"]},
        {"role": "assistant", "content": sample["output"]}
    ]
    
    # LLaMA 2 官方chat模板
    chat_template = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False
    )
    
    return {"text": chat_template}

dataset = dataset.map(format_chat_template)

def tokenize_function(sample):
    # 分词，保留labels用于计算loss
    result = tokenizer(
        sample["text"],
        truncation=True,
        max_length=512,
        padding=False,
    )
    result["labels"] = result["input_ids"].copy()
    return result

tokenized_dataset = dataset.map(
    tokenize_function,
    remove_columns=dataset.column_names,
    batched=False,
)

# ==================== 5. 训练配置 ====================
training_args = TrainingArguments(
    output_dir="./lora_checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # 有效batch = 4*4 = 16
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    evaluation_strategy="steps",
    save_total_limit=3,
    load_best_model_at_end=True,
    fp16=True,
    report_to="none",  # 不联网记录
    dataloader_num_workers=4,
    optim="paged_adamw_8bit",  # 节省显存
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, padding=True),
)

# ==================== 6. 开始训练 ====================
if __name__ == "__main__":
    trainer.train()
    
    # 保存最终模型
    model.save_pretrained("./lora_final_model")
    tokenizer.save_pretrained("./lora_final_model")
    
    # 合并权重（可选）
    # from peft import PeftModel
    # merged_model = model.merge_and_unload()
    # merged_model.save_pretrained("./merged_model")