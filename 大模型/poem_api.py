#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PoeticFlow Backend API
论文: "PoeticFlow: A Rule-Enhanced Generative Framework for 
       Classical Chinese Poetry with Stylistic Control and Prosodic Constraints"

功能:
  - 三层架构生成 (格律层 → 意象层 → 风格层)
  - 格律合规性校验 (平仄/押韵/字数)
  - 风格向量调制
  - RESTful API 接口

依赖:
  pip install flask flask-cors numpy scikit-learn

启动:
  python poeticflow_api.py
  访问: http://localhost:5000
"""

import os
import json
import random
import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional

import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS


# ============================================================
#  1. 词库与知识库
# ============================================================

# 1.1 通用词库
NOUNS = [
    "明月", "孤云", "青山", "流水", "寒松", "秋露", "暮钟", "远帆", "幽竹", "霜天",
    "玉笛", "瑶琴", "素笺", "残烛", "归雁", "石径", "松风", "渔火", "碧潭", "苍烟",
    "长亭", "古道", "西风", "瘦马", "孤灯", "晚照", "寒鸦", "落花", "疏影", "暗香",
    "香炉", "瀑布", "星河", "沧海", "浮云", "落日", "孤帆", "断鸿", "残雪", "晓风",
    "朱阁", "画栋", "玉阶", "琼楼", "瑶台", "金殿", "银阙", "铜雀", "铁马", "冰河",
    "金樽", "玉壶", "琼浆", "瑶草", "丹墀", "绣户", "珠帘", "宝鼎", "锦瑟", "琵琶",
]

VERBS = [
    "照", "流", "飞", "落", "悬", "鸣", "拂", "渡", "横", "锁",
    "卷", "摇", "坠", "舞", "绕", "映", "垂", "浮", "凝", "散",
    "倚", "望", "听", "闻", "踏", "寻", "摘", "折", "问", "思",
    "生", "挂", "下", "垂", "泻", "倾", "注", "吹", "动", "飘",
    "饮", "歌", "舞", "笑", "醉", "狂", "叹", "泣", "吟", "诵",
]

EMOTIONS = [
    "愁", "悲", "喜", "怒", "哀", "乐", "恨", "怨", "思", "念",
    "伤", "痛", "忧", "烦", "叹", "惊", "怯", "惧", "怅", "惘",
    "寂", "寞", "闲", "静", "狂", "豪", "慕", "盼", "忆", "恋",
]