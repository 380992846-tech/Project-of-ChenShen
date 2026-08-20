from jqdata import *
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
import warnings
warnings.filterwarnings('ignore')

try:
    import shap
    SHAP_AVAILABLE = True
except:
    SHAP_AVAILABLE = False
    print("SHAP not available, feature importance will use XGBoost native")

def initialize(context):
    g.stock = '510500.XSHG'
    g.position = 0
    g.entry_price = 0
    g.hold_days = 0
    g.partial_sold = False
    g.daily_returns = []
    g.prev_value = None
    
    # 核心参数
    g.atr_period = 14
    g.vol_threshold = 0.35
    g.time_stop_days = 10
    g.ml_low = 0.45
    g.ml_high = 0.55
    
    # 动态参数
    g.stop_loss = 0.035
    g.take_profit = 0.20
    g.max_days = 30
    
    # 训练数据（增量学习）
    g.X_buffer = []      # 特征缓冲区
    g.y_buffer = []      # 标签缓冲区
    g.model = None
    g.calibrated_model = None  # 概率校准模型
    g.enable_partial = True
    g.last_train_date = None    # 上次训练日期
    g.training_frequency = 5    # 每5天增量训练一次
    
    # SHAP特征重要性
    g.feature_names = ['rsi', 'pct_bb', 'vol_ratio', 'trend', 'momentum', 
                       'volatility', 'rsi_divergence', 'vol_trend', 'rel_strength',
                       'news_sentiment', 'social_sentiment']
    g.feature_importance = {}
    g.shap_values = None
    
    # LSTM情绪分析相关（简化为XGBoost）
    g.sentiment_buffer = []
    g.price_sequence = []
    g.scaler = StandardScaler()
    g.sentiment_score = 0.5
    
    # 新闻舆情数据
    g.news_cache = {}  # 缓存新闻数据
    g.social_media_cache = {}  # 缓存社交媒体数据
    
    # 增量学习参数
    g.max_buffer_size = 500  # 最大缓冲区大小
    g.min_train_samples = 50  # 最小训练样本数
    
    run_daily(trade, time='14:50')
    run_daily(report, time='15:05')
    run_daily(update_sentiment_and_news, time='09:30')  # 开盘前更新情绪
    run_daily(incremental_train, time='15:10')  # 收盘后增量训练

def get_news_sentiment(context, stock_code):
    """获取新闻舆情数据（聚宽数据源）"""
    try:
        # 使用聚宽新闻数据
        from jqdata import finance
        
        # 获取近3天的新闻
        end_date = context.current_dt.date()
        start_date = end_date - datetime.timedelta(days=3)
        
        # 查询新闻
        # news = finance.run(query(finance.NEWS).filter(
        #     finance.NEWS.stock_code == stock_code,
        #     finance.NEWS.pub_date >= start_date
        # ))
    
        # 获取融资融券余额变化（反映市场情绪）
        margin_data = get_fundamentals(
            query(valuation.code, margin.margin_balance)
            .filter(valuation.code == stock_code)
        )
        
        # 使用涨跌停家数比例（反映市场情绪）
        # 获取全市场涨跌停数据
        all_stocks = get_all_securities(['stock']).index.tolist()[:100]  # 采样
        
        up_limit_count = 0
        down_limit_count = 0
        
        for stock in all_stocks[:50]:  # 限制计算量
            try:
                df = attribute_history(stock, 1, '1d', ['close', 'high', 'low'], skip_paused=True)
                if df is not None and len(df) > 0:
                    # 简化判断涨跌停（实际需要根据ST等调整）
                    if df['close'].iloc[-1] >= df['high'].iloc[-1] * 0.995:
                        up_limit_count += 1
                    elif df['close'].iloc[-1] <= df['low'].iloc[-1] * 1.005:
                        down_limit_count += 1
            except:
                pass
        
        total = len(all_stocks[:50])
        up_ratio = up_limit_count / max(total, 1)
        down_ratio = down_limit_count / max(total, 1)
        
        # 综合情绪得分
        sentiment = 0.5
        sentiment += (up_ratio - down_ratio) * 0.3
        sentiment = np.clip(sentiment, 0, 1)
        
        return sentiment
        
    except Exception as e:
        # 如果没有新闻数据，使用量价情绪代理
        df = attribute_history(stock_code, 5, '1d', ['close', 'volume'], skip_paused=True)
        if df is not None and len(df) >= 5:
            price_change = (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]
            volume_ratio = df['volume'].iloc[-1] / (df['volume'].mean() + 1e-6)
            
            if price_change > 0.01 and volume_ratio > 1.2:
                return 0.7
            elif price_change < -0.01 and volume_ratio > 1.2:
                return 0.3
        return 0.5

def get_social_sentiment(context, stock_code):
    """获取社交媒体情绪（通过爬虫或API，这里模拟）"""
    try:
        # 实际应用中可接入：
        # 1. 微博API
        # 2. 东方财富股吧
        # 3. 雪球评论
        
        # 模拟：使用换手率作为社交媒体热度代理
        df = attribute_history(stock_code, 1, '1d', ['volume', 'money'], skip_paused=True)
        if df is not None and len(df) > 0:
            turnover_rate = df['volume'].iloc[-1] / get_float_capital(stock_code)
            
            # 换手率>3%视为热度高
            if turnover_rate > 0.03:
                return min(0.8, 0.5 + turnover_rate)
            elif turnover_rate < 0.005:
                return 0.3
        return 0.5
        
    except:
        return 0.5

def get_float_capital(stock_code):
    """获取流通股本"""
    try:
        q = query(valuation.circulating_cap).filter(valuation.code == stock_code)
        df = get_fundamentals(q)
        if len(df) > 0:
            return df['circulating_cap'].iloc[0] * 100000000  # 转换为股数
    except:
        pass
    return 1000000000  # 默认10亿股

def update_sentiment_and_news(context):
    """每日更新情绪和新闻数据"""
    stock_code = g.stock
    
    # 获取各类情绪数据
    news_sentiment = get_news_sentiment(context, stock_code)
    social_sentiment = get_social_sentiment(context, stock_code)
    
    # 综合情绪得分（新闻40% + 社交媒体30% + 市场30%）
    df = attribute_history(stock_code, 5, '1d', ['close'], skip_paused=True)
    if df is not None and len(df) >= 5:
        market_sentiment = 0.5
        if df['close'].iloc[-1] > df['close'].iloc[-2]:
            market_sentiment = 0.6
        else:
            market_sentiment = 0.4
    else:
        market_sentiment = 0.5
    
    g.sentiment_score = news_sentiment * 0.4 + social_sentiment * 0.3 + market_sentiment * 0.3
    
    # 存储到缓冲区
    g.sentiment_buffer.append(g.sentiment_score)
    if len(g.sentiment_buffer) > 10:
        g.sentiment_buffer.pop(0)

def calculate_shap_importance(model, X_sample):
    """计算SHAP特征重要性"""
    if not SHAP_AVAILABLE or model is None or X_sample is None:
        return {}
    
    try:
        # 创建解释器
        explainer = shap.Explainer(model, X_sample)
        shap_values = explainer(X_sample)
        
        # 计算平均绝对SHAP值
        importance = {}
        for i, name in enumerate(g.feature_names):
            importance[name] = np.abs(shap_values.values[:, i]).mean()
        
        # 归一化
        total = sum(importance.values())
        if total > 0:
            importance = {k: v/total for k, v in importance.items()}
        
        return importance
    except Exception as e:
        print(f"SHAP计算失败: {e}")
        return {}

def get_feature_importance_report():
    """生成特征重要性报告"""
    if not g.feature_importance:
        return "未计算特征重要性"
    
    # 排序
    sorted_importance = sorted(g.feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    report = "\n特征重要性排名（SHAP值）:\n"
    report += "-" * 40 + "\n"
    for i, (name, importance) in enumerate(sorted_importance, 1):
        bar = "█" * int(importance * 50)
        report += f"{i:2d}. {name:20s} {importance:6.2%} {bar}\n"
    
    return report

def get_features(df, df_index=None):
    """提取特征 - 11维特征（加入新闻和社交情绪）"""
    close, vol = df['close'].values, df['volume'].values
    high, low = df['high'].values, df['low'].values
    if len(close) < 50: return None
    
    # 基础指标
    ma20, std20 = np.mean(close[-20:]), np.std(close[-20:])
    rsi = lambda p: 100 - 100/(1 + (np.mean(np.maximum(np.diff(p),0)[-14:]) / 
                                     (np.mean(np.abs(np.minimum(np.diff(p),0))[-14:]) + 1e-6)))
    
    # RSI背离检测
    def check_divergence(prices, lookback=20):
        if len(prices) < lookback: return 0
        recent_prices = prices[-lookback:]
        recent_rsi = [rsi(prices[:i+1]) for i in range(len(prices)-lookback, len(prices))]
        price_min_idx = np.argmin(recent_prices)
        rsi_min_idx = np.argmin(recent_rsi)
        return 1 if (recent_prices[-1] <= recent_prices[price_min_idx] * 0.99 and 
                     recent_rsi[-1] > recent_rsi[price_min_idx] + 2) else 0
    
    # 成交量趋势
    vol_ma5 = np.mean(vol[-5:]) if len(vol) >=5 else vol[-1]
    vol_ma20 = np.mean(vol[-20:]) if len(vol) >=20 else vol[-1]
    vol_trend = vol_ma5 / vol_ma20
    
    # 行业相对强弱
    rel_strength = 0
    if df_index is not None and len(df_index) >= 50:
        zz500 = close[-1] / close[-50] - 1
        hs300 = df_index['close'].values[-1] / df_index['close'].values[-50] - 1
        rel_strength = zz500 - hs300
    
    features = {
        'rsi': rsi(close),
        'pct_bb': (close[-1] - ma20) / (std20 + 1e-6),
        'vol_ratio': vol[-1] / (vol_ma20 + 1e-6),
        'trend': close[-1] / np.mean(close[-50:]) - 1,
        'momentum': close[-1] / close[-5] - 1 if len(close) >=5 else 0,
        'atr': calc_atr(df),
        'volatility': np.std(np.diff(close[-20:])/close[-20:-1]) * np.sqrt(252),
        'rsi_divergence': check_divergence(close),
        'vol_trend': vol_trend,
        'rel_strength': rel_strength,
        'news_sentiment': g.sentiment_score,           # 新闻舆情情绪
        'social_sentiment': np.mean(g.sentiment_buffer) if g.sentiment_buffer else 0.5  # 社交情绪
    }
    
    # 情绪动量
    if len(g.sentiment_buffer) >= 5:
        features['sentiment_momentum'] = g.sentiment_buffer[-1] - g.sentiment_buffer[-5]
    else:
        features['sentiment_momentum'] = 0
    
    return features

def incremental_train(context):
    """增量学习 - 每日训练"""
    # 检查是否需要训练
    if g.last_train_date is not None:
        days_since_train = (context.current_dt.date() - g.last_train_date).days
        if days_since_train < g.training_frequency:
            return
    
    # 检查样本数量
    if len(g.X_buffer) < g.min_train_samples:
        return
    
    log.info(f"开始增量训练 | 样本数:{len(g.X_buffer)}")
    
    X = np.array(g.X_buffer)
    y = np.array(g.y_buffer)
    
    # 数据标准化
    X_scaled = g.scaler.fit_transform(X)
    
    # XGBoost参数
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': 5,
        'learning_rate': 0.05,  # 较低学习率防止过拟合
        'n_estimators': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 3,
        'gamma': 0.1,
        'reg_alpha': 0.1,  # L1正则化
        'reg_lambda': 1.0,  # L2正则化
        'scale_pos_weight': len(y) / (2 * np.sum(y) + 1e-6),  # 处理不平衡
        'random_state': 42,
        'verbosity': 0
    }
    
    # 训练模型
    model = xgb.XGBClassifier(**params)
    model.fit(X_scaled, y, 
              eval_set=[(X_scaled, y)],
              verbose=False)
    
    # 概率校准（提升预测准确度）
    g.calibrated_model = CalibratedClassifierCV(model, method='sigmoid', cv=3)
    g.calibrated_model.fit(X_scaled, y)
    g.model = g.calibrated_model
    
    # 计算特征重要性（XGBoost原生）
    xgb_importance = model.feature_importances_
    for i, name in enumerate(g.feature_names):
        g.feature_importance[name] = xgb_importance[i] / np.sum(xgb_importance)
    
    # 如果SHAP可用，计算SHAP重要性
    if SHAP_AVAILABLE and len(X) > 10:
        shap_importance = calculate_shap_importance(model, X_scaled[:min(100, len(X_scaled))])
        if shap_importance:
            # 融合XGBoost和SHAP的重要性（各50%）
            for name in g.feature_names:
                xgb_weight = g.feature_importance.get(name, 0)
                shap_weight = shap_importance.get(name, 0)
                g.feature_importance[name] = (xgb_weight + shap_weight) / 2
    
    g.last_train_date = context.current_dt.date()
    
    # 输出特征重要性
    log.info(f"增量训练完成 | 准确率:{model.score(X_scaled, y):.2%}")
    log.info(get_feature_importance_report())
    
    # 可选：减少缓冲区大小（保留最近的数据）
    if len(g.X_buffer) > g.max_buffer_size:
        keep_size = g.max_buffer_size
        g.X_buffer = g.X_buffer[-keep_size:]
        g.y_buffer = g.y_buffer[-keep_size:]

def collect_training_data(features, next_return, threshold):
    """收集训练数据"""
    if features is None:
        return
    
    feature_vector = [
        features['rsi'], features['pct_bb'], features['vol_ratio'],
        features['trend'], features['momentum'], features['volatility'],
        features['rsi_divergence'], features['vol_trend'], features['rel_strength'],
        features['news_sentiment'], features['social_sentiment']
    ]
    
    g.X_buffer.append(feature_vector)
    g.y_buffer.append(1 if next_return > threshold else 0)
    
    # 保持缓冲区大小
    if len(g.X_buffer) > g.max_buffer_size:
        g.X_buffer.pop(0)
        g.y_buffer.pop(0)

def predict_signal(features):
    """ML预测 + 多模型融合"""
    if g.model is None or features is None:
        return 0.5
    
    try:
        feature_vector = np.array([[
            features['rsi'], features['pct_bb'], features['vol_ratio'],
            features['trend'], features['momentum'], features['volatility'],
            features['rsi_divergence'], features['vol_trend'], features['rel_strength'],
            features['news_sentiment'], features['social_sentiment']
        ]])
        
        # 标准化
        feature_scaled = g.scaler.transform(feature_vector)
        
        # XGBoost预测
        xgb_prob = g.model.predict_proba(feature_scaled)[0][1]
        
        # 简单情绪动量调整
        sentiment_momentum = features.get('sentiment_momentum', 0)
        
        final_prob = xgb_prob
        
        # 情绪动量调整
        if sentiment_momentum > 0.1:
            final_prob = min(final_prob + 0.05, 0.95)
        elif sentiment_momentum < -0.1:
            final_prob = max(final_prob - 0.05, 0.05)
        
        # 不确定区间
        if g.ml_low < final_prob < g.ml_high:
            return 0.5
        
        return final_prob
    except Exception as e:
        log.error(f"预测失败: {e}")
        return 0.5

def calc_atr(df, period=14):
    """ATR计算"""
    if len(df) < period+1: return 0.02
    high, low, close = df['high'].values, df['low'].values, df['close'].values
    tr = np.maximum(high[1:]-low[1:], np.maximum(np.abs(high[1:]-close[:-1]), np.abs(low[1:]-close[:-1])))
    return np.mean(tr[-period:]) / close[-1]

def update_regime(price, ma200):
    """市场状态"""
    if price > ma200 * 1.15:
        g.take_profit, g.stop_loss, g.max_days = 0.30, 0.05, 45
        return "牛"
    elif price > ma200 * 1.05:
        g.take_profit, g.stop_loss, g.max_days = 0.20, 0.035, 30
        return "中"
    else:
        g.take_profit, g.stop_loss, g.max_days = 0.15, 0.03, 20
        return "熊"

def get_dynamic_threshold(returns, window=20):
    """动态正样本阈值"""
    if len(returns) < window:
        return 0.02
    recent_returns = returns[-window:]
    threshold = np.mean(recent_returns) + np.std(recent_returns)
    return max(threshold, 0.01)

def trade(context):
    stock = g.stock
    
    # 记录收益
    if g.prev_value is not None:
        g.daily_returns.append((context.portfolio.total_value - g.prev_value) / g.prev_value)
    g.prev_value = context.portfolio.total_value
    
    # 获取数据
    df = attribute_history(stock, 200, '1d', ['close','high','low','volume'], skip_paused=True)
    df_hs300 = attribute_history('000300.XSHG', 200, '1d', ['close'], skip_paused=True)
    if df is None or len(df) < 60: return
    
    close, price = df['close'].values, df['close'].iloc[-1]
    ma200 = np.mean(close[-200:])
    market = update_regime(price, ma200)
    
    # 收集历史收益
    all_returns = np.diff(close) / close[:-1]
    
    # 技术评分
    features = get_features(df, df_hs300)
    if features:
        rsi, bb_pos, vr = features['rsi'], features['pct_bb'], features['vol_ratio']
        score = (rsi < 45) + (bb_pos < -2) + (rsi < 30)
        if vr < 0.6 and bb_pos < -2: score += 0.5
        if vr > 1.5 and bb_pos < -2: score -= 1
        
        # 情绪因子加分
        if features['news_sentiment'] > 0.6:
            score += 1.0
        elif features['news_sentiment'] < 0.4:
            score -= 0.5
        
        # ML预测
        ml_prob = predict_signal(features)
        if ml_prob > 0.55:
            score += 1.5
        elif ml_prob < 0.45:
            score -= 0.5
        
        # 情绪动量额外加分
        if features.get('sentiment_momentum', 0) > 0.1:
            score += 0.5
        
        # 收集训练数据
        if len(all_returns) > 20:
            threshold = get_dynamic_threshold(all_returns)
            next_return = all_returns[-1] if len(all_returns) > 0 else 0
            collect_training_data(features, next_return, threshold)
    
    # 仓位管理
    can_buy = price > ma200 * 0.95
    health = check_market()
    vol = features['volatility'] if features else 0.2
    
    # 卖出逻辑
    if g.position == 1:
        g.hold_days += 1
        pnl = (price - g.entry_price) / g.entry_price
        sell = pnl < -max(g.stop_loss, calc_atr(df)*2) or pnl > g.take_profit or \
               (g.hold_days >= g.time_stop_days and pnl < 0.02) or g.hold_days > g.max_days
        
        # 情绪辅助止盈
        if not sell and g.sentiment_score > 0.85 and pnl > 0.10:
            sell = True
            log.info(f"情绪过热止盈 | 情绪:{g.sentiment_score:.2f} 收益:{pnl:.1%}")
        
        # 分批止盈
        if not sell and g.enable_partial and not g.partial_sold and pnl >= 0.15:
            shares = context.portfolio.positions[stock].total_amount
            if shares > 0:
                order_target(stock, int(shares * 0.66))
                g.partial_sold = True
                return
        
        if sell:
            order_target(stock, 0)
            g.position = g.hold_days = g.partial_sold = 0
            g.entry_price = 0
            return
    
    # 买入逻辑
    if not g.position and can_buy and score >= 2:
        pos_pct = 0.7 if score >= 3 else 0.5
        if not health: pos_pct *= 0.5
        if vol > g.vol_threshold: pos_pct *= 0.7
        
        # 模型不确定性调整
        ml_prob = predict_signal(features) if features else 0.5
        if 0.45 < ml_prob < 0.55:
            pos_pct *= 0.5
            log.info(f"模型不确定({ml_prob:.2f})，仓位减半")
        
        # 情绪极度悲观时逆向加仓
        if features and features['news_sentiment'] < 0.25:
            pos_pct = min(pos_pct * 1.3, 0.95)
            log.info(f"市场情绪极度悲观，逆向加仓")
        
        order_target_value(stock, context.portfolio.total_value * pos_pct)
        g.position, g.entry_price, g.hold_days, g.partial_sold = 1, price, 0, False
        log.info(f"买入|s:{score:.1f} ml:{ml_prob:.2f} sent:{features['news_sentiment']:.2f} p:{pos_pct:.0%} {market}")

def check_market():
    """大盘健康度"""
    df = attribute_history('000300.XSHG', 20, '1d', ['close'], skip_paused=True)
    if df is None or len(df) < 20: return True
    close = df['close'].values
    return close[-1] > np.mean(close[-10:]) > np.mean(close[-20:]) * 0.98

def report(context):
    """周报 - XGBoost+SHAP增强版"""
    if context.current_dt.weekday() != 4: return
    
    val, start = context.portfolio.total_value, context.portfolio.starting_cash
    df = attribute_history('510500.XSHG', len(range(context.run_params.start_date.day)),
                           '1d', ['close'], skip_paused=True)
    
    if df is not None and len(df) > 0:
        start_price = df['close'].iloc[0] if len(df) > 0 else 1
        end_price = df['close'].iloc[-1]
        bench = (end_price / start_price - 1) * 100
        ret = (val / start - 1) * 100
        
        log.info("=" * 60)
        log.info(f"XGBoost量化策略周报 | {context.current_dt.strftime('%Y-%m-%d')}")
        log.info(f"策略:{ret:.2f}% vs 中证500:{bench:.2f}% | 超额:{ret-bench:.2f}%")
        
        if len(g.daily_returns) >= 20:
            recent = g.daily_returns[-20:]
            sharpe = np.sqrt(252) * np.mean(recent) / (np.std(recent) + 1e-6)
            win = sum(1 for r in recent if r > 0) / len(recent)
            log.info(f"夏普比率:{sharpe:.2f} | 胜率:{win:.1%} | 训练样本:{len(g.X_buffer)}")
            log.info(f"综合情绪:{g.sentiment_score:.2f} | 模型状态:{'已训练' if g.model else '训练中'}")
            
            # 输出特征重要性
            if g.feature_importance:
                log.info(get_feature_importance_report())
        
        log.info("=" * 60)
