"""models 包：Transformer 模型定义与配置。"""
from .config import ModelConfig
from .gpt import GPT, GPTConfig

__all__ = ["ModelConfig", "GPT", "GPTConfig"]
