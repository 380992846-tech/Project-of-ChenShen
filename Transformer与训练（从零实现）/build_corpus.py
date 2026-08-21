"""
build_corpus.py — 转发入口

语料构建已迁移到 `data/build_corpus.py`。本文件保留以兼容旧调用，
内部直接调用新模块。
"""

from __future__ import annotations

from data.build_corpus import main

if __name__ == "__main__":
    main()
