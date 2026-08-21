"""models/config.py — 超参数配置（dataclass + YAML 加载）

所有实验超参数集中在类型化 dataclass 中，可从 ``config.yaml`` 加载，
也可在命令行用 ``--key value`` 覆盖（见 train.py）。这比硬编码更利于实验管理。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ModelConfig:
    """模型结构超参数。"""

    vocab_size: int = 1899      # 词表大小（训练时按语料自动覆写）
    n_layer: int = 4
    n_head: int = 4
    n_embd: int = 128
    block_size: int = 128       # 最大上下文长度
    dropout: float = 0.0


@dataclass
class TrainConfig:
    """训练超参数。"""

    steps: int = 2000
    batch: int = 32
    lr: float = 3e-3
    eval_every: int = 250
    gen_len: int = 60
    grad_clip: float = 1.0
    seed: int = 0
    sample_prompts: list[str] = field(default_factory=lambda: ["清华", "他", "如果"])


@dataclass
class DataConfig:
    """数据超参数。"""

    seq_len: int = 128
    corpus: str = "training_data.txt"   # 训练语料文件
    val_ratio: float = 0.1              # 验证集比例


@dataclass
class Config:
    """汇总配置。"""

    model: ModelConfig = field(default_factory=ModelConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    data: DataConfig = field(default_factory=DataConfig)


def _merge(base: dict, overrides: dict) -> dict:
    """浅层合并，overrides 覆盖 base 的同名键。"""
    out = dict(base)
    for k, v in overrides.items():
        if v is not None:
            out[k] = v
    return out


def load_config(yaml_path: str | Path | None = None) -> Config:
    """从 YAML 文件加载配置；文件缺失或未指定时用默认值。

    YAML 结构约定::

        model:
          n_embd: 128
        train:
          steps: 3000
        data:
          seq_len: 128
    """
    model_defaults = asdict(ModelConfig())
    train_defaults = asdict(TrainConfig())
    data_defaults = asdict(DataConfig())

    if yaml_path is not None and Path(yaml_path).exists():
        import yaml

        with open(yaml_path, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
    else:
        raw = {}

    model_cfg = _merge(model_defaults, raw.get("model", {}))
    train_cfg = _merge(train_defaults, raw.get("train", {}))
    data_cfg = _merge(data_defaults, raw.get("data", {}))

    return Config(
        model=ModelConfig(**model_cfg),
        train=TrainConfig(**train_cfg),
        data=DataConfig(**data_cfg),
    )
