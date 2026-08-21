"""
dashboard.py — Transformer 训练监控仪表盘（Streamlit）

从 `complete_ai_toolkit.py` 拆出的监控面板，展示训练曲线、模型信息、在线生成。

用法
----
.. code-block:: bash

    streamlit run dashboard.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

st.set_page_config(page_title="Transformer 训练监控", layout="wide")
st.title("Transformer 训练监控仪表盘")

# 侧边栏配置
with st.sidebar:
    st.header("超参数配置")
    learning_rate = st.slider("学习率", 0.0001, 0.01, 0.001, 0.0001)
    num_layers = st.slider("Transformer 层数", 1, 8, 4)
    batch_size = st.selectbox("批次大小", [16, 32, 64, 128])

    st.header("生成控制")
    temperature = st.slider("温度参数", 0.1, 2.0, 0.8, 0.05)
    gen_length = st.slider("生成长度", 50, 500, 200)

col1, col2 = st.columns(2)

with col1:
    st.subheader("训练曲线")
    history_file = HERE / "训练报告.md"
    # 从训练报告 md 中读取，简单展示；实际可读取 CSV/log
    if history_file.exists():
        st.info("训练报告已生成，见 `训练报告.md`")
        st.image(str(HERE / "training_curve.png"), use_column_width=True)
    else:
        st.info("暂无训练数据，请先运行 train.py")

with col2:
    st.subheader("模型信息")
    best = HERE / "checkpoints" / "best_char_gpt.pth"
    if best.exists():
        st.success("模型已训练")
        st.metric("模型大小", f"{best.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        st.warning("未找到训练好的模型（checkpoints/best_char_gpt.pth）")

    st.subheader("在线生成")
    prompt = st.text_input("输入提示词", "机器学习")
    if st.button("生成"):
        st.info("生成中…（请用 generate.py 在命令行运行）")
        st.code(f"python generate.py --prompt \"{prompt}\" --length {gen_length}")
