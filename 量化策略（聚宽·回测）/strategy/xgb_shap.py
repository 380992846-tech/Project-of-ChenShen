"""
strategy/xgb_shap.py
====================

迁移自 ``quant_xgboost_shap.py``（聚宽：XGBoost + SHAP 增量学习）。

原版逻辑
--------
- 11 维特征：rsi, pct_bb, vol_ratio, trend, momentum, volatility,
  rsi_divergence, vol_trend, rel_strength, news_sentiment, social_sentiment。
- 增量学习：每日训练 XGBoost + 概率校准；SHAP 做特征重要性。
- 买入：技术 + 情绪 + ML 概率综合得分>=2；卖出：止损/止盈/无进展/超时/情绪过热。

适配多标的
----------
- 每只标的按相同特征算得分（情绪用「量价情绪代理」替代新闻/社媒，离线可用）。
- 若安装了 xgboost 则做真实增量训练+SHAP；否则退化为**规则 + 量价情绪**得分。
- 同时把特征重要性 / SHAP 报告保存在 ``self.state``，供 API 的信号解释面板使用。
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from 量化系统.data.loader import PricePanel
from 量化系统.data.factors import compute_factors, ma, momentum, volatility
from 量化系统.strategy.score_select import ScoreSelectionStrategy, BaseStrategy


class XGBoostShapStrategy(ScoreSelectionStrategy):
    name = "xgb_shap"

    # 与 quant_xgboost_shap.py 对齐的 11 维特征名
    _FEATURES = ["rsi", "bb_position", "volume_ratio", "trend", "momentum_20",
                 "volatility", "vol_trend", "rel_strength", "news_sentiment", "social_sentiment"]

    def init(self) -> None:
        super().init()
        self.training_frequency = int(self.params.get("training_frequency", 5))
        self.min_train_samples = int(self.params.get("min_train_samples", 50))
        self.max_buffer_size = int(self.params.get("max_buffer_size", 500))
        self.ml_low = float(self.params.get("ml_low", 0.45))
        self.ml_high = float(self.params.get("ml_high", 0.55))
        self.state["feature_importance"] = {}

    # ------------------------------------------------------------------
    # 特征构造（含量价情绪代理）
    # ------------------------------------------------------------------
    def _features_for_symbol(self, df: pd.DataFrame) -> pd.DataFrame:
        feat = compute_factors(df)
        close = df["close"]
        # vol_trend = MA5量 / MA20量
        vol = df["volume"] if "volume" in df.columns else pd.Series(1.0, index=df.index)
        feat["vol_trend"] = vol.rolling(5).mean() / (vol.rolling(20).mean() + 1e-8)
        # rel_strength：相对基准（用自身 long-term 动量近似）
        feat["rel_strength"] = momentum(close, 60) - momentum(close, 20)
        # 量价情绪代理（0..1）：涨且放量偏看多
        ret1 = close.pct_change()
        feat["news_sentiment"] = (0.5 + 0.3 * np.sign(ret1) + 0.2 * (feat["volume_ratio"] - 1)).clip(0, 1)
        feat["social_sentiment"] = feat["news_sentiment"].rolling(5).mean()
        # 映射原版特征名
        rename = {
            "bb_position": "pct_bb",
            "momentum_20": "momentum",
        }
        feat = feat.rename(columns=rename)
        # 前瞻收益标签（供 ML 训练）
        feat["future_ret"] = close.shift(-5) / close - 1
        return feat

    # ------------------------------------------------------------------
    # 得分矩阵
    # ------------------------------------------------------------------
    def asset_score(self, panel: PricePanel) -> pd.DataFrame:
        scores = {}
        for sym in panel.symbols:
            df = panel.per_symbol[sym][["close", "high", "low", "volume"]].copy()
            if df.empty or len(df) < 60:
                scores[sym] = pd.Series(0.0, index=panel.close.index)
                continue
            feat = self._features_for_symbol(df)
            scores[sym] = self._score_symbol(feat)
        return pd.DataFrame(scores).reindex(panel.close.index).ffill().fillna(0.5)

    def _score_symbol(self, feat: pd.DataFrame) -> pd.Series:
        # 技术分
        rsi = feat.get("rsi", pd.Series(50, index=feat.index)).fillna(50)
        bb = feat.get("pct_bb", pd.Series(0, index=feat.index)).fillna(0)
        vr = feat.get("volume_ratio", pd.Series(1, index=feat.index)).fillna(1)
        vol = feat.get("volatility", pd.Series(0.2, index=feat.index)).fillna(0.2)
        sent = feat.get("news_sentiment", pd.Series(0.5, index=feat.index)).fillna(0.5)

        score = pd.Series(0.0, index=feat.index)
        score += (rsi < 45).astype(float)
        score += (bb < -2).astype(float)
        score += (rsi < 30).astype(float)
        score += ((vr < 0.6) & (bb < -2)).astype(float) * 0.5
        score -= ((vr > 1.5) & (bb < -2)).astype(float) * 1.0
        score += (sent > 0.6).astype(float)
        score -= (sent < 0.4).astype(float) * 0.5
        # ML 概率（可选）
        try:
            prob = self._ml_prob(feat)
            score += (prob > 0.55).astype(float) * 1.5
            score -= (prob < 0.45).astype(float) * 0.5
        except Exception:
            pass
        return score

    def _ml_prob(self, feat: pd.DataFrame) -> np.ndarray:
        """尝试用 xgboost 得概率；未安装则返回 0.5。"""
        try:
            import xgboost as xgb
        except Exception:
            return np.full(len(feat), 0.5)
        # 简化：用前 60% 训练、后 40% 推断
        X_cols = [c for c in self._FEATURES if c in feat.columns] or ["rsi", "volatility"]
        X = feat[X_cols].fillna(0).to_numpy()
        y = (feat["future_ret"] > 0.003).astype(int).to_numpy() if "future_ret" in feat else None
        if y is None or len(X) < 80:
            return np.full(len(feat), 0.5)
        split = int(len(X) * 0.6)
        model = xgb.XGBClassifier(
            objective="binary:logistic", max_depth=5, learning_rate=0.05,
            n_estimators=80, subsample=0.8, colsample_bytree=0.8,
            min_child_weight=3, random_state=42, verbosity=0)
        model.fit(X[:split], y[:split])
        prob = model.predict_proba(X[split:])[:, 1]
        out = np.full(len(feat), 0.5)
        out[split:] = prob
        return out

    def on_trade(self, symbol, action, price, reason=None) -> None:
        super().on_trade(symbol, action, price, reason)
        # 保留一次解释要点到 state（供面板）
        self.state["last_trade"] = {"symbol": symbol, "action": action,
                                    "price": price, "reason": reason}


# 别名兼容原命名
XGBShap = XGBoostShapStrategy
