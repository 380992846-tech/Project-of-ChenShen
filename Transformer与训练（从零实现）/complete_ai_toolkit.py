# ==================== complete_ai_toolkit.py ====================
# 兼容入口：原"全家桶"已按职责拆分为独立模块。
#
#   训练      -> train.py（字符级 GPT，GPU / CPU / DDP）
#   生成      -> generate.py
#   RAG 问答  -> rag.py
#   量化      -> quantize.py
#   监控面板  -> dashboard.py
#
# 本文件仅作为平滑迁移的转发入口，按需惰性导入，避免顶层依赖（如 streamlit）。

__all__ = ["run_training", "run_generate", "run_rag", "run_quantize", "run_dashboard"]

_MODULES = {
    "run_training": ("train", "main"),
    "run_generate": ("generate", "main"),
    "run_rag": ("rag", "main"),
    "run_quantize": ("quantize", "main"),
}


def __getattr__(name):
    if name in _MODULES:
        mod_name, func_name = _MODULES[name]
        import importlib
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def run_dashboard():
    """启动监控面板。"""
    import os
    os.system("streamlit run dashboard.py")


if __name__ == "__main__":
    print(
        "complete_ai_toolkit.py 已拆分为独立模块：\n"
        "  python train.py            # 训练\n"
        "  python generate.py         # 生成\n"
        "  python rag.py              # RAG\n"
        "  python quantize.py         # 量化\n"
        "  streamlit run dashboard.py # 监控面板\n"
    )
