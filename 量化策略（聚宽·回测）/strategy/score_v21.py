"""
strategy/score_v21.py
=====================

迁移自 ``quant_v21.py``（聚宽：打分制 + 动态止盈止损）。

原版逻辑
--------
- 打分：RSI<45 (+1)，价格<布林下轨*1.08 (+1)，RSI<30 (+1)，
  缩量下跌（vol_ratio<0.6 且低价）(+0.5)，放量下跌(-1)，RSI底背离(+1.5)。
- 大盘健康过滤、波动率过滤（高波动降仓）。
- 评分>=2 开仓，>=3 仓位 70%，否则 50%；不健康/高波动再降。
- 根据价格相对 MA200 动态调整止盈/止损/最大持仓。

适配多标的
----------
- 对每只标的独立打分（大盘健康用基准指数近似）。
- 开仓选得分最高的标的；得分转成 0..1 概率供 ScoreSelectionStrategy 门槛化。
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from 量化系统.data.loader import PricePanel
from 量化系统.strategy.score_select import ScoreSelectionStrategy, BaseStrategy


class ScoreStrategyV21(ScoreSelectionStrategy):
    name = "score_v21"

    def init(self) -> None:
        super().init()
        self.rsi_buy = float(self.params.get("rsi_buy", 45))
        self.bb_factor = float(self.params.get("bb_factor", 1.08))
        self.vol_ratio_threshold = float(self.params.get("vol_ratio_threshold", 0.6))
        self.volatility_threshold = float(self.params.get("volatility_threshold", 0.35))
        self.time_stop_days = int(self.params.get("time_stop_days", 10))
        self.time_stop_min_pnl = float(self.params.get("time_stop_min_pnl", 0.02))
        self.enable_divergence = bool(self.params.get("enable_divergence", True))

    # 得分矩阵 = 规则得分 / 5，规到 0..1
    def asset_score(self, panel: PricePanel) -> pd.DataFrame:
        scores = {}
        for sym in panel.symbols:
            df = panel.per_symbol[sym]
            score = self._score_symbol(df)
            scores[sym] = score
        mat = pd.DataFrame(scores).reindex(panel.close.index).ffill()
        # 规整到 0..1（原最大约 5 分）
        return (mat / 5.0).clip(0.0, 1.0).fillna(0.0)

    def _score_symbol(self, df: pd.DataFrame) -> pd.Series:
        close = df["close"]
        rsi = df["rsi"] if "rsi" in df.columns else pd.Series(50, index=df.index)
        bb = df["bb_position"] if "bb_position" in df.columns else pd.Series(0.5, index=df.index)
        vr = df["volume_ratio"] if "volume_ratio" in df.columns else pd.Series(1.0, index=df.index)
        # 布林下轨 ~ bb_position 低代表接近下轨
        score = pd.Series(0.0, index=df.index)
        score += (rsi < self.rsi_buy).astype(float)
        score += (rsi < 30).astype(float)
        # 价格接近/低于布林下轨：bb_position 越小越接近下轨
        score += (bb < 0.0).astype(float) * 1.0
        # 成交量确认
        score += ((vr < self.vol_ratio_threshold) & (bb < 0.3)).astype(float) * 0.5
        score -= ((vr > 1.5) & (bb < 0.3)).astype(float) * 1.0
        # 底背离近似：RSI 新低但价格未新低（用简单判定）
        if self.enable_divergence:
            score += self._divergence_bonus(close, rsi)
        return score

    @staticmethod
    def _divergence_bonus(close: pd.Series, rsi: pd.Series, lookback: int = 20) -> pd.Series:
        """RSI 底背离加分：最近 lookback 内 RSI 低点对应的价格高于价格低点。"""
        out = pd.Series(0.0, index=close.index)
        c, r = close.to_numpy(), rsi.to_numpy()
        for i in range(lookback, len(close)):
            wc, wr = c[i - lookback + 1:i + 1], r[i - lookback + 1:i + 1]
            p_low = int(np.argmin(wc))
            r_low = int(np.argmin(wr))
            if p_low != r_low and wc[p_low] < wc[r_low] and wr[p_low] > wr[r_low]:
                out.iloc[i] = 1.5
        return out


# 别名兼容原命名
ScoreV21 = ScoreStrategyV21
