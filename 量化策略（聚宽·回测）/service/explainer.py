"""
service/explainer.py
====================

交易信号自然语言解释。

设计原则
--------
- **缺省模板化**：不依赖外部 LLM，直接从因子/特征/持仓上下文拼出可读、可解释的中文说明。
  - 若策略给出了特征重要性（XGBoost/SHAP），优先引用「最影响当前信号的因子」。
  - 否则用因子即时值（RSI/动量/波动/量比/趋势）解释。
- **可选 LLM 增强**：当配置了 ``llm.endpoint`` 时，把信号上下文连同 prompt 发给 LLM，
  生成更自然的一段话。可配置 ``llm.enabled``。

后端接口：见 ``api/server.py`` 的 ``GET /api/signals/explain``。
"""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from 量化系统.config import get_settings
from 量化系统.service.logging_setup import get_logger

logger = get_logger(__name__)


# --------------------------------------------------------------------------
# 因子 -> 中文描述
# --------------------------------------------------------------------------
_FACTOR_LABELS = {
    "rsi": "RSI",
    "momentum_20": "20日动量",
    "momentum_60": "60日动量",
    "ma_bias": "均线乖离",
    "volatility": "波动率",
    "trend": "趋势",
    "volume_ratio": "量比",
    "turnover": "换手",
    "bb_position": "布林带位置",
    "atr": "ATR/价格",
}

_RULE_HINTS: dict[str, str] = {
    "rsi": "RSI 高位(>70)则超买，<30 则超卖",
    "momentum_20": "20日动量为正代表中期走强",
    "ma_bias": "正乖离偏离长期均线越高越可能回归",
    "volatility": "波动率越高仓位应越谨慎",
    "volume_ratio": "量比高代表放量，缩量常视为洗盘",
    "trend": "MA20>MA60 视为多头趋势",
    "bb_position": "布林带下轨附近具备反弹条件",
}


def _describe_factor(name: str, value: float) -> str:
    label = _FACTOR_LABELS.get(name, name)
    hint = _RULE_HINTS.get(name, "")
    if pd.isna(value):
        return f"{label}：暂无数据"
    return f"{label}={value:.2f}" + (f"（{hint}）" if hint else "")


# --------------------------------------------------------------------------
# 构建上下文
# --------------------------------------------------------------------------
class Explainer:
    """从一次交易信号/持仓上下文构造解释。

    参数
    ----
    feature_importance : 策略可能给出的 {factor: importance}（如 XGBoost/SHAP）。
    factor_values : {factor: value}，用于填充解释。
    llm_client : 可选的 LLM 客户端（具备 ``generate(prompt) -> str``）。
    """

    def __init__(
        self,
        feature_importance: dict[str, float] | None = None,
        factor_values: dict[str, float] | None = None,
        llm_client: Any | None = None,
    ):
        self.feature_importance = feature_importance or {}
        self.factor_values = factor_values or {}
        self.llm_client = llm_client
        self.settings = get_settings()

    # ------------------------------------------------------------------
    # 模板化解释
    # ------------------------------------------------------------------
    def explain(self, symbol: str, action: str, price: float | None = None,
                reason: str | None = None, weight: float | None = None) -> dict[str, Any]:
        """返回结构化 + 自然语言解释。"""
        reasons = self._build_reasons()
        template = self._template_text(symbol, action, price, reason, weight, reasons)

        result: dict[str, Any] = {
            "symbol": symbol,
            "action": action,
            "price": price,
            "reason": reason,
            "weight": weight,
            "explanation": template,
            "factors": [{"name": k, "label": _FACTOR_LABELS.get(k, k), "value": round(v, 3)}
                        for k, v in self.factor_values.items()],
            "top_factors": [{"name": k, "importance": round(v, 3)}
                            for k, v in sorted(self.feature_importance.items(),
                                               key=lambda x: -x[1])[:5]],
        }

        # 可选：LLM 增强
        if self.llm_client is not None:
            try:
                llm_text = self.llm_client.generate(self._build_prompt(result))
                if llm_text:
                    result["llm_explanation"] = llm_text
            except Exception as exc:  # noqa: BLE001
                logger.warning("LLM 解释失败，使用模板：%s", exc)
        return result

    # ------------------------------------------------------------------
    # 依据
    # ------------------------------------------------------------------
    def _build_reasons(self) -> list[str]:
        reasons: list[str] = []
        # 按重要性排序的关键因子
        top = sorted(self.feature_importance.items(), key=lambda x: -x[1])[:3]
        for name, imp in top:
            value = self.factor_values.get(name)
            if pd.isna(value):
                continue
            reasons.append(f"{_FACTOR_LABELS.get(name, name)}是重要因子（权重{imp:.0%}），当前值 {value:.2f}")
        if not reasons:
            # 退化为默认因子说明
            for name in ["rsi", "momentum_20", "volatility", "trend", "volume_ratio"]:
                if name in self.factor_values:
                    reasons.append(_describe_factor(name, self.factor_values[name]))
        return reasons[:4]

    # ------------------------------------------------------------------
    # 模板文本
    # ------------------------------------------------------------------
    def _template_text(self, symbol, action, price, reason, weight, reasons) -> str:
        action_cn = "买入" if action == "buy" else "卖出"
        direction = "看多" if action == "buy" else "看空/止盈"
        price_txt = f"，参考价 {price:.3f}" if price is not None else ""
        weight_txt = f"，计划仓位 {weight:.0%}" if weight is not None else ""
        reason_txt = f"；触发原因：{reason}" if reason else ""

        if reasons:
            basis = "；".join(reasons)
            body = f"针对标的 {symbol} {action_cn}信号（{direction}{price_txt}{weight_txt}）。" \
                   f"主要依据：{basis}。{reason_txt}"
        else:
            body = f"针对标的 {symbol} 的{action_cn}信号（{direction}{price_txt}{weight_txt}）。{reason_txt}"
        return body

    # ------------------------------------------------------------------
    # LLM prompt（若启用）
    # ------------------------------------------------------------------
    def _build_prompt(self, result: dict[str, Any]) -> str:
        context = {
            "symbol": result["symbol"],
            "action": result["action"],
            "price": result["price"],
            "reason": result["reason"],
            "weight": result["weight"],
            "factors": result["factors"],
            "top_factors": result["top_factors"],
        }
        prompt = (
            "你是一个A股TMT板块量化分析师。请用简洁、专业、不带投资建议的口吻，"
            "解释下面这条交易信号为什么会触发，并提示风险。不超过80字。\n"
            f"信号上下文：{json.dumps(context, ensure_ascii=False)}\n"
        )
        return prompt


# --------------------------------------------------------------------------
# 默认 LLM 客户端（用 requests 调 OpenAI 兼容端点）
# --------------------------------------------------------------------------
class SimpleLLMClient:
    """一个极简 LLM 客户端：POST 到 OpenAI 兼容的 /chat/completions。

    需要配置 ``config.yaml`` 的 ``llm: {enabled, endpoint, api_key, model}``。
    不配置则无需 LLM，系统仍用模板解释。
    """

    def __init__(self, endpoint: str, api_key: str | None = None, model: str = "gpt-4o-mini"):
        import requests
        self._requests = requests
        self.endpoint = endpoint
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str | None:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 200,
        }
        resp = self._requests.post(
            f"{self.endpoint.rstrip('/')}/v1/chat/completions", json=payload,
            headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def build_explainer(
    feature_importance: dict[str, float] | None = None,
    factor_values: dict[str, float] | None = None,
) -> Explainer:
    """按配置构造 :class:`Explainer`（含可选 LLM 客户端）。"""
    settings = get_settings()
    llm_client = None
    cfg = getattr(settings, "llm", None)
    if cfg is not None and getattr(cfg, "enabled", False):
        llm_client = SimpleLLMClient(cfg.endpoint, cfg.api_key, cfg.model)
    return Explainer(feature_importance, factor_values, llm_client)
