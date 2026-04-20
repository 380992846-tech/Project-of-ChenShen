# ==================== optimized_ai_toolkit.py ====================
# 优化版：解决胡言乱语问题，增加多种生成策略

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import argparse
import os
import json
import time
import random
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ==================== 1. 文档处理模块 ====================
class DocumentProcessor:
    """处理.docx和.txt文档"""
    
    @staticmethod
    def read_docx(file_path):
        try:
            from docx import Document
            doc = Document(file_path)
            full_text = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n'.join(full_text)
        except ImportError:
            print("⚠️ python-docx未安装")
            return ""
        except Exception as e:
            print(f"读取失败 {file_path}: {e}")
            return ""
    
    @staticmethod
    def read_txt(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.read()
            except:
                return ""
    
    @classmethod
    def build_corpus(cls, file_paths):
        all_texts = []
        for path in file_paths:
            if not os.path.exists(path):
                print(f"⚠️ 文件不存在: {path}")
                continue
            if path.endswith('.docx'):
                text = cls.read_docx(path)
            elif path.endswith('.txt'):
                text = cls.read_txt(path)
            else:
                continue
            if text:
                all_texts.append(text)
                print(f"✓ 已加载: {path} ({len(text):,} 字符)")
        
        combined = '\n\n'.join(all_texts)
        with open('training_data.txt', 'w', encoding='utf-8') as f:
            f.write(combined)
        return combined

# ==================== 2. 改进的Transformer模型 ====================
class ImprovedCharTransformer(nn.Module):
    """改进版：增加dropout和正则化防止过拟合"""
    
    def __init__(self, vocab_size, d_model=256, nhead=8, num_layers=6, 
                 max_len=1024, dropout=0.2):
        super().__init__()
        
        self.vocab_size = vocab_size
        self.d_model = d_model
        
        # 增强的embedding
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.dropout_emb = nn.Dropout(dropout)
        
        # 可学习的位置编码
        self.pos_encoding = nn.Parameter(torch.randn(1, max_len, d_model) * 0.02)
        
        # Transformer编码器（增加dropout）
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            dim_feedforward=d_model * 4,
            batch_first=True, 
            dropout=dropout,
            activation='gelu'  # GELU激活函数效果更好
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 输出层
        self.layer_norm = nn.LayerNorm(d_model)
        self.fc_out = nn.Linear(d_model, vocab_size)
        
        # 初始化权重
        self._init_weights()
    
    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x):
        seq_len = min(x.shape[1], self.pos_encoding.shape[1])
        embedded = self.embedding(x)
        embedded = embedded + self.pos_encoding[:, :seq_len, :]
        embedded = self.dropout_emb(embedded)
        
        out = self.transformer(embedded)
        out = self.layer_norm(out)
        logits = self.fc_out(out)
        return logits

# ==================== 3. 数据集类 ====================
class CharDataset(Dataset):
    def __init__(self, text, seq_len=128, stride=None, char_to_idx=None):
        self.seq_len = seq_len
        self.stride = stride or seq_len // 2
        
        if char_to_idx is None:
            chars = sorted(list(set(text)))
            self.char_to_idx = {ch: i for i, ch in enumerate(chars)}
            self.idx_to_char = {i: ch for ch, i in self.char_to_idx.items()}
            self.vocab_size = len(chars)
        else:
            self.char_to_idx = char_to_idx
            self.idx_to_char = {i: ch for ch, i in char_to_idx.items()}
            self.vocab_size = len(char_to_idx)
        
        self.data = torch.tensor([self.char_to_idx.get(ch, 0) for ch in text], dtype=torch.long)
        
        self.xs = []
        self.ys = []
        for i in range(0, len(self.data) - seq_len - 1, self.stride):
            self.xs.append(self.data[i:i+seq_len])
            self.ys.append(self.data[i+1:i+seq_len+1])
    
    def __len__(self):
        return len(self.xs)
    
    def __getitem__(self, idx):
        return self.xs[idx], self.ys[idx]

# ==================== 4. 改进的生成函数（核心优化）====================
def smart_generate(model, start_str, char_to_idx, idx_to_char, 
                   length=300, temperature=0.6, top_k=40, top_p=0.9,
                   repetition_penalty=1.2, device='cpu'):
    """
    智能生成：解决胡言乱语问题
    - temperature: 降低到0.6以下更稳定
    - top_k: 只从概率最高的k个字符中采样
    - top_p: 核采样，累积概率达到p后截断
    - repetition_penalty: 惩罚重复字符
    """
    model.eval()
    
    # 转换起始字符串
    chars = [char_to_idx.get(ch, 0) for ch in start_str]
    input_ids = torch.tensor(chars).unsqueeze(0).to(device)
    generated = start_str
    
    # 记录已生成的字符（用于重复惩罚）
    recent_chars = []
    
    # 有效字符集合（排除特殊符号和空格过多）
    valid_chars = set('的一是不了人在我有他这个们中来上大为到和地出得也时小可对生能而子过年发后作里用道行所然者方于法从定现看去前如还进样同把开手把机学理工量数化算据型模方结果分度间'
                      'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    
    for _ in range(length):
        if input_ids.shape[1] > 512:
            input_ids = input_ids[:, -512:]
        
        with torch.no_grad():
            output = model(input_ids)
            logits = output[0, -1, :].clone()  # 复制避免修改原tensor
            
            # 1. 重复惩罚
            for i, char_idx in enumerate(recent_chars[-10:]):  # 惩罚最近10个字符
                penalty = repetition_penalty ** (1.0 / (i + 1))
                logits[char_idx] /= penalty
            
            # 2. 惩罚无效字符（降低标点、特殊符号的概率）
            for idx, ch in idx_to_char.items():
                if ch not in valid_chars and ch not in '。！？；：""''、，.！？；：""''':
                    logits[idx] *= 0.5
            
            # 3. 温度调节
            logits = logits / temperature
            
            # 4. Top-K采样
            if top_k > 0:
                indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
                logits[indices_to_remove] = float('-inf')
            
            # 5. Top-P (nucleus) 采样
            if top_p < 1.0:
                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                
                # 移除累积概率超过top_p的token
                sorted_indices_to_remove = cumulative_probs > top_p
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                sorted_indices_to_remove[..., 0] = 0
                
                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[indices_to_remove] = float('-inf')
            
            # 6. 采样
            probs = torch.softmax(logits, dim=-1)
            
            # 避免NaN
            if torch.isnan(probs).any():
                probs = torch.ones_like(probs) / len(probs)
            
            next_char_idx = torch.multinomial(probs, 1).item()
        
        next_char = idx_to_char[next_char_idx]
        generated += next_char
        input_ids = torch.cat([input_ids, torch.tensor([[next_char_idx]]).to(device)], dim=1)
        
        # 更新最近字符记录
        recent_chars.append(next_char_idx)
        if len(recent_chars) > 20:
            recent_chars.pop(0)
        
        # 可选：如果连续生成相同字符超过3次，强制打断
        if len(generated) > 3 and len(set(generated[-3:])) == 1:
            # 插入一个空格或句号
            forced_char = '。' if next_char != '。' else '，'
            generated = generated[:-1] + forced_char
            input_ids = input_ids[:, :-1]
            input_ids = torch.cat([input_ids, torch.tensor([[char_to_idx.get(forced_char, 0)]]).to(device)], dim=1)
    
    return generated

# ==================== 5. 批处理生成 ====================
def batch_generate(model, prompts, char_to_idx, idx_to_char, 
                   length=200, temperature=0.6, device='cpu'):
    """批量生成"""
    results = []
    for prompt in prompts:
        result = smart_generate(model, prompt, char_to_idx, idx_to_char,
                               length=length, temperature=temperature, device=device)
        results.append(result)
    return results

# ==================== 6. 训练函数（改进版）====================
def train_model_improved(model, train_loader, val_loader, epochs=50, lr=0.001, device='cpu'):
    """改进的训练函数，带学习率调度和早停"""
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    
    # 余弦退火学习率调度
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    best_val_loss = float('inf')
    patience = 10
    patience_counter = 0
    history = {'train_loss': [], 'val_loss': []}
    
    print(f"\n开始训练...")
    print(f"设备: {device}")
    print("="*60)
    
    for epoch in range(epochs):
        # 训练
        model.train()
        total_train_loss = 0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            predictions = model(batch_x)
            loss = criterion(predictions.reshape(-1, model.vocab_size), batch_y.reshape(-1))
            
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            total_train_loss += loss.item()
        
        # 验证
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                predictions = model(batch_x)
                loss = criterion(predictions.reshape(-1, model.vocab_size), batch_y.reshape(-1))
                total_val_loss += loss.item()
        
        avg_train_loss = total_train_loss / len(train_loader)
        avg_val_loss = total_val_loss / len(val_loader)
        scheduler.step()
        
        history['train_loss'].append(avg_train_loss)
        history['val_loss'].append(avg_val_loss)
        
        # 保存最佳模型
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), 'best_model.pth')
            patience_counter = 0
            print(f"✓ 保存最佳模型 (loss: {avg_val_loss:.4f})")
        else:
            patience_counter += 1
        
        # 早停
        if patience_counter >= patience:
            print(f"早停于 epoch {epoch+1}")
            break
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")
    
    # 保存训练历史
    with open('training_history.json', 'w') as f:
        json.dump(history, f)
    
    return model, history

# ==================== 7. 模型评估函数 ====================
def evaluate_model(model, char_to_idx, idx_to_char, device='cpu'):
    """评估模型生成质量"""
    test_prompts = [
        "机器学习",
        "量化投资",
        "黑洞",
        "深度学习"
    ]
    
    print("\n" + "="*60)
    print("模型评估 - 不同温度下的生成效果")
    print("="*60)
    
    temperatures = [0.3, 0.5, 0.7, 0.9]
    
    for prompt in test_prompts:
        print(f"\n提示词: {prompt}")
        print("-"*40)
        
        for temp in temperatures:
            result = smart_generate(model, prompt, char_to_idx, idx_to_char,
                                   length=150, temperature=temp, device=device)
            # 只显示前100字
            preview = result[:100].replace('\n', ' ')
            print(f"T={temp}: {preview}...")
        print("-"*40)

# ==================== 8. 交互式生成 ====================
def interactive_generate(model, char_to_idx, idx_to_char, device='cpu'):
    """交互式生成"""
    print("\n" + "="*60)
    print("交互式生成模式")
    print("输入提示词，输入 'quit' 退出")
    print("="*60)
    
    while True:
        prompt = input("\n提示词: ").strip()
        if prompt.lower() == 'quit':
            break
        
        # 可选参数
        try:
            temp = float(input("温度 (0.3-1.0, 默认0.6): ") or "0.6")
            temp = max(0.3, min(1.0, temp))
        except:
            temp = 0.6
        
        try:
            length = int(input("生成长度 (100-500, 默认200): ") or "200")
            length = max(100, min(500, length))
        except:
            length = 200
        
        print("\n生成中...")
        result = smart_generate(model, prompt, char_to_idx, idx_to_char,
                               length=length, temperature=temp, device=device)
        print(f"\n生成结果:\n{result}")

# ==================== 9. 主训练流程 ====================
def main():
    print("="*60)
    print("优化版字符级Transformer训练")
    print("="*60)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    # 文档路径
    doc_files = [
        '贵系.docx',
        '量化.docx', 
        '宇宙与物理规律.docx'
    ]
    
    # 检查文件
    print("\n检查文档文件...")
    for f in doc_files:
        if os.path.exists(f):
            print(f"✓ 找到: {f}")
        else:
            print(f"❌ 文件不存在: {f}")
            return
    
    # 加载文档
    print("\n加载文档...")
    processor = DocumentProcessor()
    text = processor.build_corpus(doc_files)
    
    print(f"总字符数: {len(text):,}")
    
    # 创建数据集
    print("\n创建数据集...")
    dataset = CharDataset(text, seq_len=256, stride=128)
    
    # 划分训练/验证集
    train_size = int(0.9 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)
    
    print(f"训练样本: {train_size}, 验证样本: {val_size}")
    print(f"词汇表大小: {dataset.vocab_size}")
    
    # 创建模型
    print("\n创建模型...")
    model = ImprovedCharTransformer(
        vocab_size=dataset.vocab_size,
        d_model=256,
        nhead=8,
        num_layers=6,
        max_len=1024,
        dropout=0.2
    )
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"模型参数量: {total_params:,}")
    
    # 训练
    model, history = train_model_improved(
        model, train_loader, val_loader,
        epochs=50, lr=0.001, device=device
    )
    
    # 保存词汇表
    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump({
            'char_to_idx': dataset.char_to_idx,
            'idx_to_char': {str(k): v for k, v in dataset.idx_to_char.items()}
        }, f, ensure_ascii=False)
    
    # 评估模型
    evaluate_model(model, dataset.char_to_idx, dataset.idx_to_char, device)
    
    # 进入交互模式
    interactive_generate(model, dataset.char_to_idx, dataset.idx_to_char, device)
    
    print("\n✅ 完成！")

# ==================== 10. 加载已有模型进行生成 ====================
def load_and_generate(model_path='best_model.pth', vocab_path='vocab.json'):
    """加载已有模型并生成"""
    print("加载模型...")
    
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    char_to_idx = vocab['char_to_idx']
    idx_to_char = {int(k): v for k, v in vocab['idx_to_char'].items()}
    
    model = ImprovedCharTransformer(vocab_size=len(char_to_idx))
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    print(f"✓ 模型加载成功，词汇表大小: {len(char_to_idx)}")
    
    # 交互式生成
    interactive_generate(model, char_to_idx, idx_to_char, device)

# ==================== 11. 运行 ====================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='train',
                        choices=['train', 'generate'])
    parser.add_argument('--prompt', type=str, default='机器学习')
    parser.add_argument('--length', type=int, default=300)
    parser.add_argument('--temperature', type=float, default=0.6)
    args = parser.parse_args()
    
    if args.mode == 'train':
        main()
    else:
        # 单次生成模式
        with open('vocab.json', 'r', encoding='utf-8') as f:
            vocab = json.load(f)
        char_to_idx = vocab['char_to_idx']
        idx_to_char = {int(k): v for k, v in vocab['idx_to_char'].items()}
        
        model = ImprovedCharTransformer(vocab_size=len(char_to_idx))
        model.load_state_dict(torch.load('best_model.pth', map_location='cpu'))
        model.eval()
        
        result = smart_generate(model, args.prompt, char_to_idx, idx_to_char,
                               length=args.length, temperature=args.temperature)
        print(result)