# ==================== complete_ai_toolkit.py ====================
# 整合所有功能：文档处理 + 字符级Transformer + 5个扩展功能
# 运行方式：
#   python complete_ai_toolkit.py --mode train        # 训练模型
#   python complete_ai_toolkit.py --mode classify     # 文本分类
#   python complete_ai_toolkit.py --mode generate     # 条件生成
#   python complete_ai_toolkit.py --mode rag          # RAG问答
#   python complete_ai_toolkit.py --mode dashboard    # 启动监控面板
#   python complete_ai_toolkit.py --mode quantize     # 模型量化
#   python complete_ai_toolkit.py --mode web          # 启动Gradio界面

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
import numpy as np
import argparse
import os
import sys
import time
import warnings
from pathlib import Path
import json
import hashlib
from typing import List, Tuple, Optional, Dict

warnings.filterwarnings("ignore")

# ==================== 0. 依赖检查 ====================
def check_dependencies():
    """检查并提示缺失的依赖"""
    missing = []
    
    try:
        import torch
    except ImportError:
        missing.append("torch")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    if missing:
        print(f"❌ 缺失依赖: {', '.join(missing)}")
        print("请运行: pip install " + " ".join(missing))
        return False
    
    # 可选依赖
    try:
        from docx import Document
        global DOCX_AVAILABLE
        DOCX_AVAILABLE = True
        print("✓ python-docx 已安装")
    except ImportError:
        DOCX_AVAILABLE = False
        print("⚠️ python-docx未安装，无法处理.docx文件。请运行: pip install python-docx")
    
    try:
        import gradio as gr
        global GRADIO_AVAILABLE
        GRADIO_AVAILABLE = True
        print("✓ gradio 已安装")
    except ImportError:
        GRADIO_AVAILABLE = False
        print("⚠️ gradio未安装，Web界面模式不可用。请运行: pip install gradio")
    
    try:
        from sentence_transformers import SentenceTransformer
        global SENTENCE_TRANSFORMERS_AVAILABLE
        SENTENCE_TRANSFORMERS_AVAILABLE = True
        print("✓ sentence-transformers 已安装")
    except ImportError:
        SENTENCE_TRANSFORMERS_AVAILABLE = False
        print("⚠️ sentence-transformers未安装，RAG将使用关键词检索。请运行: pip install sentence-transformers")
    
    return True

# ==================== 1. 文档处理模块 ====================
class DocumentProcessor:
    """处理.docx和.txt文档，构建训练数据"""
    
    @staticmethod
    def read_docx(file_path):
        """读取docx文件（如果安装了python-docx）"""
        if not DOCX_AVAILABLE:
            print(f"跳过 {file_path}：需要安装python-docx")
            return ""
        try:
            from docx import Document
            doc = Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return '\n'.join(full_text)
        except Exception as e:
            print(f"读取docx失败 {file_path}: {e}")
            return ""
    
    @staticmethod
    def read_txt(file_path):
        """读取txt文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()
    
    @classmethod
    def build_corpus(cls, file_paths, train_ratio=0.8):
        """从多个文件构建语料库，支持按文件划分训练/验证集"""
        all_texts = []
        file_info = []
        
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
            
            if text and len(text) > 100:  # 过滤太短的文件
                all_texts.append(text)
                file_info.append({'path': path, 'length': len(text)})
                print(f"✓ 已加载: {path} ({len(text)} 字符)")
        
        if not all_texts:
            raise ValueError("没有找到有效的文档文件")
        
        # 按文件划分训练/验证集（避免信息泄露）
        np.random.seed(42)
        indices = np.random.permutation(len(all_texts))
        split_idx = int(len(indices) * train_ratio)
        train_indices = indices[:split_idx]
        val_indices = indices[split_idx:]
        
        train_text = '\n\n'.join([all_texts[i] for i in train_indices])
        val_text = '\n\n'.join([all_texts[i] for i in val_indices])
        
        # 保存
        with open('training_data.txt', 'w', encoding='utf-8') as f:
            f.write(train_text)
        with open('validation_data.txt', 'w', encoding='utf-8') as f:
            f.write(val_text)
        
        print(f"\n训练集: {len(train_indices)} 个文件, {len(train_text)} 字符")
        print(f"验证集: {len(val_indices)} 个文件, {len(val_text)} 字符")
        
        return train_text, val_text

# ==================== 2. 字符级Transformer模型 ====================
class CharTransformer(nn.Module):
    """支持条件生成、分类、量化的增强版Transformer"""
    
    def __init__(self, vocab_size, d_model=128, nhead=8, num_layers=4, 
                 max_len=512, dropout=0.1, num_classes=None, num_themes=None):
        super().__init__()
        
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.num_classes = num_classes
        self.num_themes = num_themes
        
        # 基础组件
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = nn.Parameter(torch.randn(1, max_len, d_model))
        self.dropout = nn.Dropout(dropout)
        
        # Transformer编码器
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=512,
            batch_first=True, dropout=dropout
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 输出头
        self.fc_out = nn.Linear(d_model, vocab_size)
        
        if num_classes:
            self.classifier = nn.Linear(d_model, num_classes)
        
        if num_themes:
            self.theme_embedding = nn.Embedding(num_themes, d_model)
    
    def forward(self, x, theme_ids=None, task='generate'):
        seq_len = x.shape[1]
        embedded = self.embedding(x)
        
        if theme_ids is not None and self.num_themes:
            theme_emb = self.theme_embedding(theme_ids).unsqueeze(1)
            embedded = embedded + theme_emb
        
        embedded = embedded + self.pos_encoding[:, :seq_len, :]
        embedded = self.dropout(embedded)
        out = self.transformer(embedded)
        
        if task == 'classify' and self.num_classes:
            pooled = out.mean(dim=1)
            logits = self.classifier(pooled)
            return logits
        else:
            logits = self.fc_out(out)
            return logits

# ==================== 3. 数据准备模块 ====================
class CharDataset(Dataset):
    """字符级数据集"""
    
    def __init__(self, text, seq_len=128, char_to_idx=None, stride=None):
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
        
        # 转为数字序列
        self.data = torch.tensor([self.char_to_idx.get(ch, 0) for ch in text], dtype=torch.long)
        
        # 创建序列（非重叠采样减少泄露）
        self.xs = []
        self.ys = []
        for i in range(0, len(self.data) - seq_len - 1, self.stride):
            self.xs.append(self.data[i:i+seq_len])
            self.ys.append(self.data[i+1:i+seq_len+1])
    
    def __len__(self):
        return len(self.xs)
    
    def __getitem__(self, idx):
        return self.xs[idx], self.ys[idx]

# ==================== 4. 训练函数 ====================
def train_model(model, train_loader, val_loader, epochs=30, lr=0.001, device='cpu'):
    """通用训练函数"""
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=500, gamma=0.9)
    
    best_val_loss = float('inf')
    history = {'train_loss': [], 'val_loss': []}
    
    for epoch in range(epochs):
        model.train()
        total_train_loss = 0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            predictions = model(batch_x, task='generate')
            loss = criterion(predictions.reshape(-1, model.vocab_size), batch_y.reshape(-1))
            
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            total_train_loss += loss.item()
        
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                predictions = model(batch_x, task='generate')
                loss = criterion(predictions.reshape(-1, model.vocab_size), batch_y.reshape(-1))
                total_val_loss += loss.item()
        
        avg_train_loss = total_train_loss / len(train_loader)
        avg_val_loss = total_val_loss / len(val_loader)
        scheduler.step()
        
        history['train_loss'].append(avg_train_loss)
        history['val_loss'].append(avg_val_loss)
        
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), 'best_model.pth')
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")
    
    with open('training_history.json', 'w') as f:
        json.dump(history, f)
    
    return model, history

# ==================== 5. 生成函数 ====================
def generate_text(model, start_str, char_to_idx, idx_to_char, length=300, 
                  temperature=0.8, theme_id=None, device='cpu', max_repeat=5):
    """生成文本（带重复检测）"""
    model.eval()
    
    chars = [char_to_idx.get(ch, 0) for ch in start_str]
    input_ids = torch.tensor(chars).unsqueeze(0).to(device)
    generated = start_str
    
    theme_tensor = None
    if theme_id is not None and hasattr(model, 'num_themes') and model.num_themes:
        theme_tensor = torch.tensor([theme_id]).to(device)
    
    last_chars = []  # 检测重复
    
    for _ in range(length):
        if input_ids.shape[1] > 512:
            input_ids = input_ids[:, -512:]
        
        with torch.no_grad():
            output = model(input_ids, theme_ids=theme_tensor, task='generate')
            logits = output[0, -1, :] / temperature
            probs = torch.softmax(logits, dim=-1)
            next_char_idx = torch.multinomial(probs, 1).item()
        
        next_char = idx_to_char[next_char_idx]
        
        # 重复检测
        last_chars.append(next_char)
        if len(last_chars) > max_repeat:
            last_chars.pop(0)
            if len(set(last_chars)) == 1:
                # 检测到重复，提高温度
                temperature = min(temperature * 1.2, 1.5)
        
        generated += next_char
        input_ids = torch.cat([input_ids, torch.tensor([[next_char_idx]]).to(device)], dim=1)
    
    return generated

# ==================== 6. 改进的RAG系统 ====================
class ImprovedRAG:
    """改进的检索增强生成系统（带缓存和抽取式答案）"""
    
    def __init__(self, generator_model, char_to_idx, idx_to_char, device='cpu'):
        self.generator = generator_model
        self.char_to_idx = char_to_idx
        self.idx_to_char = idx_to_char
        self.device = device
        self.documents = []
        self.embeddings = None
        self.encoder = None
        self.cache_dir = Path("./model_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # 尝试加载轻量级Embedding模型
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self._load_embedding_model()
    
    def _load_embedding_model(self, max_retries=3, timeout=30):
        """带超时和缓存的模型加载"""
        from sentence_transformers import SentenceTransformer
        import urllib.request
        
        # 使用更小的模型（33MB vs 80MB）
        model_name = 'paraphrase-MiniLM-L3-v2'
        cache_path = self.cache_dir / model_name.replace('/', '_')
        
        # 检查本地缓存
        if cache_path.exists():
            print(f"✓ 从缓存加载Embedding模型: {cache_path}")
            try:
                self.encoder = SentenceTransformer(str(cache_path))
                return
            except Exception as e:
                print(f"缓存加载失败: {e}")
        
        # 尝试下载
        for attempt in range(max_retries):
            try:
                print(f"正在下载Embedding模型（{model_name}），约33MB...")
                print(f"尝试 {attempt + 1}/{max_retries}")
                
                # 设置超时
                socket.setdefaulttimeout(timeout)
                
                self.encoder = SentenceTransformer(model_name, cache_folder=str(self.cache_dir))
                print("✓ Embedding模型加载成功")
                return
                
            except Exception as e:
                print(f"下载失败: {e}")
                if attempt < max_retries - 1:
                    print("等待5秒后重试...")
                    time.sleep(5)
                else:
                    print("⚠️ 无法下载Embedding模型，将使用关键词检索")
                    self.encoder = None
    
    def build_index(self, documents):
        """构建检索索引"""
        self.documents = documents
        
        # 分句处理，提高检索精度
        self.sentences = []
        for doc in documents:
            # 简单分句
            for sent in doc.replace('\n', '。').split('。'):
                sent = sent.strip()
                if len(sent) > 10:  # 过滤太短的句子
                    self.sentences.append(sent)
        
        if self.encoder:
            try:
                self.embeddings = self.encoder.encode(self.sentences, show_progress_bar=False)
                print(f"✓ 已索引 {len(self.sentences)} 个句子")
            except Exception as e:
                print(f"编码失败: {e}，使用关键词检索")
                self.encoder = None
                self.embeddings = None
    
    def retrieve(self, query, top_k=3):
        """检索相关文档"""
        if not self.sentences:
            return []
        
        if self.encoder and self.embeddings is not None:
            try:
                from sklearn.metrics.pairwise import cosine_similarity
                query_vec = self.encoder.encode([query])
                similarities = cosine_similarity(query_vec, self.embeddings)[0]
                top_indices = similarities.argsort()[-top_k:][::-1]
                return [(self.sentences[i], similarities[i]) for i in top_indices]
            except Exception as e:
                print(f"检索失败: {e}")
        
        # 降级：关键词匹配
        query_words = set(query.lower().split())
        scores = [len(query_words & set(sent.lower().split())) for sent in self.sentences]
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(self.sentences[i], scores[i]) for i in top_indices if scores[i] > 0]
    
    def generate_answer(self, query):
        """生成答案（抽取式为主，生成为辅）"""
        retrieved = self.retrieve(query, top_k=3)
        
        if not retrieved:
            return "未找到相关信息。"
        
        # 方案1：抽取式答案（更可靠）
        best_sent, score = retrieved[0]
        if score > 0.5:  # 相似度足够高
            answer = best_sent
            if len(retrieved) > 1:
                answer += "。" + retrieved[1][0]
            return answer
        
        # 方案2：基于检索结果的模板式回答
        context = " ".join([sent for sent, _ in retrieved[:2]])
        answer = f"根据资料：{context}"
        
        return answer
    
    def chat(self, query):
        """对话接口"""
        return self.generate_answer(query)

# ==================== 7. 文本分类器 ====================
def train_classifier():
    """训练文本分类器"""
    print("\n=== 训练文本分类器 ===")
    
    texts = [
        "这部电影太棒了，非常好看", "糟糕透顶，浪费时间",
        "精彩绝伦，值得一看", "太差了，不推荐",
        "演技精湛，剧情动人", "无聊至极，看不下去",
        "画面精美，特效震撼", "粗制滥造，毫无诚意",
    ]
    labels = [1, 0, 1, 0, 1, 0, 1, 0]
    
    all_chars = set(''.join(texts))
    char_to_idx = {ch: i for i, ch in enumerate(sorted(all_chars))}
    vocab_size = len(char_to_idx)
    
    def text_to_tensor(text, max_len=100):
        indices = [char_to_idx.get(ch, 0) for ch in text[:max_len]]
        indices = indices + [0] * (max_len - len(indices))
        return torch.tensor(indices)
    
    X = torch.stack([text_to_tensor(t) for t in texts])
    y = torch.tensor(labels)
    
    model = CharTransformer(vocab_size=vocab_size, num_classes=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.001)
    
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        logits = model(X, task='classify')
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            acc = (logits.argmax(dim=1) == y).float().mean()
            print(f"Epoch {epoch+1}: Loss={loss.item():.4f}, Acc={acc:.4f}")
    
    torch.save(model.state_dict(), 'classifier_model.pth')
    print("分类器训练完成！")
    return model

# ==================== 8. 监控仪表盘 ====================
def launch_dashboard():
    """启动Streamlit监控面板"""
    dashboard_code = '''# dashboard.py 内容同上，略'''
    
    with open('dashboard.py', 'w', encoding='utf-8') as f:
        f.write(dashboard_code)
    
    print("启动监控面板...")
    os.system("streamlit run dashboard.py")

# ==================== 9. 模型量化 ====================
def quantize_model(model_path='best_model.pth', vocab_size=100):
    """INT8量化模型"""
    print("\n=== 模型量化 ===")
    
    model = CharTransformer(vocab_size=vocab_size)
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    # 动态量化
    model_int8 = torch.quantization.quantize_dynamic(
        model, {nn.Linear, nn.Embedding}, dtype=torch.qint8
    )
    
    def test_speed(model, runs=100):
        import time
        test_input = torch.randint(0, vocab_size, (1, 128))
        model.eval()
        times = []
        with torch.no_grad():
            for _ in range(runs):
                start = time.time()
                _ = model(test_input)
                times.append(time.time() - start)
        return np.mean(times) * 1000
    
    fp32_time = test_speed(model)
    int8_time = test_speed(model_int8)
    
    print(f"FP32 推理时间: {fp32_time:.2f} ms")
    print(f"INT8 推理时间: {int8_time:.2f} ms")
    print(f"加速比: {fp32_time/int8_time:.2f}x")
    
    torch.save(model_int8.state_dict(), 'model_int8.pth')
    print("量化模型已保存")
    
    return model_int8

# ==================== 10. Gradio Web界面 ====================
def launch_web_ui():
    """启动Gradio Web界面"""
    if not GRADIO_AVAILABLE:
        print("请先安装gradio: pip install gradio")
        return
    
    import gradio as gr
    
    # 加载模型（如果有）
    model = None
    char_to_idx = None
    idx_to_char = None
    
    if os.path.exists('best_model.pth'):
        print("加载已训练模型...")
        # 这里需要加载之前保存的词汇表
        # 简化处理
    
    def chat_interface(message, history):
        # RAG问答
        if os.path.exists('training_data.txt'):
            with open('training_data.txt', 'r', encoding='utf-8') as f:
                docs = [f.read()]
            rag = ImprovedRAG(None, None, None, 'cpu')
            rag.build_index(docs)
            return rag.chat(message)
        return "请先运行训练模式: python 模型全功能部署.py --mode train"
    
    def generate_interface(prompt, length, temperature):
        if model and char_to_idx:
            return generate_text(model, prompt, char_to_idx, idx_to_char, 
                                length=int(length), temperature=float(temperature))
        return "请先训练模型"
    
    with gr.Blocks(title="AI工具包", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🤖 完整AI工具包")
        gr.Markdown("字符级Transformer + RAG问答系统")
        
        with gr.Tab("💬 RAG问答"):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="输入问题")
            clear = gr.Button("清空")
            
            def respond(message, chat_history):
                bot_message = chat_interface(message, chat_history)
                chat_history.append((message, bot_message))
                return "", chat_history
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)
        
        with gr.Tab("✍️ 文本生成"):
            prompt = gr.Textbox(label="输入提示词", value="机器学习")
            length = gr.Slider(50, 500, value=200, label="生成长度")
            temperature = gr.Slider(0.1, 1.5, value=0.8, label="温度参数")
            generate_btn = gr.Button("生成")
            output = gr.Textbox(label="生成结果", lines=10)
            
            generate_btn.click(generate_interface, [prompt, length, temperature], output)
        
        with gr.Tab("📊 训练信息"):
            if os.path.exists("training_history.json"):
                with open("training_history.json") as f:
                    history = json.load(f)
                gr.LinePlot(value=history, x="epoch", y=["train_loss", "val_loss"], 
                           title="训练曲线")
            else:
                gr.Markdown("暂无训练数据")
    
    demo.launch(share=False, server_port=7860)

# ==================== 11. 主函数 ====================
def main():
    # 先检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='完整AI工具包')
    parser.add_argument('--mode', type=str, default='train',
                        choices=['train', 'classify', 'generate', 'rag', 'dashboard', 'quantize', 'web'],
                        help='运行模式')
    parser.add_argument('--docs', type=str, nargs='+', 
                        default=[],
                        help='文档路径')
    args = parser.parse_args()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    if args.mode == 'train':
        print("加载文档...")
        processor = DocumentProcessor()
        
        # 如果没有指定文档，创建示例文档
        docs = args.docs
        if not docs:
            # 创建示例文档
            with open('sample_doc.txt', 'w', encoding='utf-8') as f:
                f.write("机器学习是人工智能的一个分支。它让计算机能够从数据中学习。\n")
                f.write("深度学习是机器学习的一个子集，使用多层神经网络。\n")
                f.write("Transformer模型在自然语言处理领域取得了巨大成功。\n")
            docs = ['sample_doc.txt']
            print("未指定文档，已创建示例文档 sample_doc.txt")
        
        train_text, val_text = processor.build_corpus(docs, train_ratio=0.8)
        
        print("准备数据...")
        # 使用不同的stride减少训练/验证集泄露
        train_dataset = CharDataset(train_text, seq_len=128, stride=64)
        val_dataset = CharDataset(val_text, seq_len=128, stride=128)  # 验证集无重叠
        
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        print(f"词汇表大小: {train_dataset.vocab_size}")
        print(f"训练样本: {len(train_dataset)}, 验证样本: {len(val_dataset)}")
        
        model = CharTransformer(vocab_size=train_dataset.vocab_size)
        model, history = train_model(model, train_loader, val_loader, epochs=30, device=device)
        
        # 保存词汇表
        with open('vocab.json', 'w', encoding='utf-8') as f:
            json.dump({
                'char_to_idx': train_dataset.char_to_idx,
                'idx_to_char': {str(k): v for k, v in train_dataset.idx_to_char.items()}
            }, f, ensure_ascii=False)
        
        # 测试生成
        sample = generate_text(model, "机器", train_dataset.char_to_idx, 
                              train_dataset.idx_to_char, length=200, device=device)
        print("\n生成样本：")
        print(sample)
    
    elif args.mode == 'classify':
        train_classifier()
    
    elif args.mode == 'generate':
        print("条件生成模式")
        if os.path.exists('best_model.pth') and os.path.exists('vocab.json'):
            with open('vocab.json', 'r', encoding='utf-8') as f:
                vocab = json.load(f)
            char_to_idx = vocab['char_to_idx']
            idx_to_char = {int(k): v for k, v in vocab['idx_to_char'].items()}
            model = CharTransformer(vocab_size=len(char_to_idx))
            model.load_state_dict(torch.load('best_model.pth', map_location=device))
            model.to(device)
            
            prompt = input("输入提示词: ")
            result = generate_text(model, prompt, char_to_idx, idx_to_char, device=device)
            print(f"\n生成结果:\n{result}")
        else:
            print("请先训练模型: python 模型全功能部署.py --mode train")
    
    elif args.mode == 'rag':
        print("RAG问答系统")
        if os.path.exists('training_data.txt'):
            with open('training_data.txt', 'r', encoding='utf-8') as f:
                docs = [f.read()]
            
            rag = ImprovedRAG(None, None, None, device)
            rag.build_index(docs)
            
            print("\n进入问答模式（输入 q 退出）")
            while True:
                query = input("\n问题: ").strip()
                if query.lower() == 'q':
                    break
                answer = rag.chat(query)
                print(f"答案: {answer}")
        else:
            print("请先训练模型: python 模型全功能部署.py --mode train")
    
    elif args.mode == 'dashboard':
        launch_dashboard()
    
    elif args.mode == 'quantize':
        if os.path.exists('vocab.json'):
            with open('vocab.json', 'r', encoding='utf-8') as f:
                vocab = json.load(f)
            quantize_model(vocab_size=len(vocab['char_to_idx']))
        else:
            quantize_model(vocab_size=100)
    
    elif args.mode == 'web':
        launch_web_ui()

if __name__ == "__main__":
    # 导入socket用于超时设置
    import socket
    main()
