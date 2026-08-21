"""test_config.py — 配置加载测试。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.config import load_config  # noqa: E402


def test_default_config():
    """无文件时返回默认配置。"""
    cfg = load_config(None)
    assert cfg.model.n_embd == 128
    assert cfg.train.steps == 2000
    assert cfg.data.seq_len == 128


def test_load_real_yaml():
    """读取项目 config.yaml。"""
    p = Path(__file__).resolve().parent.parent / "config.yaml"
    cfg = load_config(p)
    assert cfg.model.n_embd > 0
    assert cfg.train.batch > 0
    assert len(cfg.train.sample_prompts) >= 1
