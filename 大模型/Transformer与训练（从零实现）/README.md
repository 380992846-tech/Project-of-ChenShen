# Transformer 与训练（从零实现）

> 手把手从零实现 Transformer，并在**真实中文语料**上训练出一个会生成中文的模型。

## 为什么做这个项目

"会调用大模型"和"懂大模型"是两回事。这个项目的目的，是**不依赖现成框架地**把
Transformer 写一遍——Embedding、多头注意力、位置编码、训练循环、生成采样——
并在 `training_data.txt`（中文语料）上真正训练，看到损失下降、困惑度降低、
模型能吐出中文片段。

## 项目组成

| 文件 | 作用 | 定位 |
|------|------|------|
| `train.py` | ★ **在真实中文语料上训练字符级 GPT**：损失曲线 / 困惑度 / checkpoint / 生成样例 | 核心实战 |
| `build_corpus.py` | 从 `笔记/` 的《贵系》《量化》《宇宙与物理规律》三个 docx 抽取合并成语料 | 数据构建 |
| `complete_ai_toolkit.py` | 字符级 Transformer 全家桶（训练/分类/生成/RAG/量化/监控面板） | 多功能工具箱 |
| `mini_transformer.py` | 极简 Transformer，学习算术序列 `[a,b,c]→[b,c,a+b]` 模式 | 入门教学 demo |
| `training_data.txt` | 中文训练语料（`build_corpus.py` 生成，贵系+量化+宇宙物理，111K 字符） | 数据 |
| `vocab.json` | 字符级词表 | 数据 |
| `训练报告.md` | 训练损失、困惑度、生成样例与结论 | 报告 |

## 核心：`train.py` 训练字符级 GPT

在真实中文语料上训练 **decoder-only GPT**（模型复用仓库内 `大模型/llm/gpt.py` 的从零实现）。

```bash
python 大模型/Transformer与训练（从零实现）/train.py --steps 2000 --n_embd 128 --n_layer 4
```

**做了什么**
1. 读 `training_data.txt` → 建字符词表 → 按 9:1 切 train/val；
2. 训练，记录 train/val 损失，`models/` 存最佳 checkpoint；
3. 训练中每若干步生成中文样例，直观看到进展；
4. 结束输出**困惑度 PPL** + 生成样例 + 损失曲线（`training_curve.png`）+ `训练报告.md`。

**结果**（CPU 训练，详见 `训练报告.md`）：困惑度远低于随机基线（≈词表大小），
损失持续下降，生成出短句级通顺的中文片段——证明从零实现的 Transformer 真的学会了语言统计规律。

## 理解链路（建议学习顺序）

1. **`mini_transformer.py`** — 先用算术序列看懂"Transformer 怎么学一个规律"；
2. **`complete_ai_toolkit.py`** — 看一个完整的字符级 Transformer 能扩展出多少能力（RAG/量化/监控）；
3. **`train.py`** — 在真实中文上训练，看到"从零实现的模型"真正生成中文。

## 复现与扩展

```bash
# 训练（调大 steps / n_embd / n_layer 以提升质量）
python 大模型/Transformer与训练（从零实现）/train.py --steps 3000 --n_embd 192 --n_layer 6

# 用生成的中文片段感受模型
# （可进一步写 generate.py 加载 models/best_char_gpt.pth 做纯推理）
```

> ⚠️ 训练产物（`models/*.pth`）已被 `.gitignore` 排除，不会进版本库，随时可重新训练。
> 小模型 + CPU + 有限步数下生成的是短句级通顺片段；要更长更连贯，需更大模型 / GPU / 更多语料。
