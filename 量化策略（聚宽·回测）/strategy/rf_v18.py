"""
strategy/rf_v18.py
==================

迁移自 ``joinquant_v18.py``（聚宽：随机森林策略）。

原版逻辑
--------
- 特征：ret_1d/5d/20d, bias(ma20), vol_ratio, volatility, rsi, trend。
- 用最近 N 天数据训练 RandomForest，预测「未来5日涨幅>0.5%」概率。
- 开仓：trend==1 且 prob > 阈值，满仓（max_position）。
- 平仓：止损 / 移动止损 / 超时 / 趋势走弱。

适配到多标的
------------
- 对每只标的用相同的特征与标签（未来5日收益>阈值→正样本）。
- 每只标的独立走随机森林 walk-forward（按年重训，离线合成数据足够）。
- 若未安装 sklearn，退化为**基于趋势+RSI+量比的规则得分**，保证离线可跑。
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from 量化系统.data.loader import PricePanel
from 量化系统.data.factors import compute_factors, add_labels
from 量化系统.strategy.score_select import ScoreSelectionStrategy, BaseStrategy


class RandomForestV18(ScoreSelectionStrategy):
    name = "rf_v18"

    # v18 用到的特征列（在 factors 中都有）
    _FEATURES = ["ret_1d", "ret_5d", "ret_20d", "ma_bias", "volume_ratio",
                 "volatility", "rsi", "trend"]

    def init(self) -> None:
        super().init()
        self.forward_days = int(self.params.get("forward_days", 5))
        self.label_threshold = float(self.params.get("label_threshold", 0.005))
        self.train_window = int(self.params.get("train_window", 500))

    def asset_score(self, panel: PricePanel) -> pd.DataFrame:
        scores: dict[str, pd.Series] = {}
        for sym in panel.symbols:
            df = panel.per_symbol[sym][["close", "high", "low", "volume"]].copy()
            if df.empty or len(df) < 60:
                scores[sym] = pd.Series(0.0, index=panel.close.index)
                continue
            feat = compute_factors(df)
            # add_labels 需要 close 列做前瞻标签
            feat["close"] = df["close"]
            feat = add_labels(feat, self.forward_days, self.label_threshold)
            if len(feat) < 100:
                scores[sym] = pd.Series(0.0, index=panel.close.index)
                continue
            scores[sym] = self._walk_forward_prob(feat)
        return pd.DataFrame(scores).reindex(panel.close.index).ffill().fillna(0.5)

    def _walk_forward_prob(self, feat: pd.DataFrame) -> pd.Series:
        """按年 walk-forward 的随机森林（或规则）得分。"""
        X_cols = [c for c in self._FEATURES if c in feat.columns]
        prob = pd.Series(0.5, index=feat.index)
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler
            HAS_SKLEARN = True
        except Exception:
            HAS_SKLEARN = False

        if not HAS_SKLEARN:
            # 规则得分：趋势（0/1）+ RSI 低位 + 动量
            trend = feat.get("trend", pd.Series(0, index=feat.index)).fillna(0)
            rsi = feat.get("rsi", pd.Series(50, index=feat.index)).fillna(50)
            mom20 = feat.get("ret_20d", pd.Series(0, index=feat.index)).fillna(0)
            rule = 0.4 * trend + 0.3 * (rsi < 40).astype(float) + 0.3 * (mom20 > 0).astype(float)
            return rule.clip(0.0, 1.0).reindex(feat.index)

        years = sorted(feat.index.year.unique())
        for i in range(1, len(years)):
            train = feat[feat.index.year.isin(years[:i])]
            test = feat[feat.index.year == years[i]]
            if len(train) < 100 or len(test) < 20:
                continue
            Xtr = train[X_cols].values
            ytr = train["label"].values
            Xte = test[X_cols].values
            if np.isnan(Xtr).any() or np.isnan(Xte).any():
                continue
            scaler = StandardScaler()
            Xtr_s = scaler.fit_transform(Xtr)
            Xte_s = scaler.transform(Xte)
            model = RandomForestClassifier(
                n_estimators=100, max_depth=6, min_samples_split=20,
                min_samples_leaf=10, random_state=42, n_jobs=-1)
            model.fit(Xtr_s, ytr)
            p = model.predict_proba(Xte_s)[:, 1]
            prob.loc[test.index] = p

        return prob.clip(0.0, 1.0)


# 别名兼容原命名
RFV18 = RandomForestV18
