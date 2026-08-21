from jqdata import *
import numpy as np

def initialize(context):
    g.stock = '510300.XSHG'
    g.position = 0
    g.entry_price = 0
    g.hold_days = 0
    g.partial_sold = False      # 分批止盈标记
    
    # ===== V21参数（V20修复版）=====
    # 基础参数
    g.base_stop_loss = 0.035
    g.base_take_profit = 0.20
    g.max_hold_days = 30
    g.rsi_buy = 45
    g.bb_factor = 1.08
    
    # 动态参数（会在交易中根据市场状态调整）
    g.current_stop_loss = g.base_stop_loss
    g.current_take_profit = g.base_take_profit
    g.current_max_hold_days = g.max_hold_days
    
    # ATR相关
    g.atr_period = 14
    
    # 成交量相关
    g.volume_ratio_threshold = 0.6
    
    # 功能开关
    g.enable_divergence = True      # RSI底背离
    g.enable_time_stop = True       # 无进展止损
    g.enable_partial_profit = True  # 分批止盈
    g.enable_market_filter = True   # 大盘环境过滤
    g.enable_volatility_filter = True # 波动率过滤
    
    # 阈值参数
    g.volatility_threshold = 0.35   # 波动率阈值
    g.time_stop_days = 10           # 无进展止损天数
    g.time_stop_min_pnl = 0.02      # 无进展止损最低收益
    
    # 记录每日收益率（用于夏普计算）
    g.daily_returns = []
    
    run_daily(trade, time='14:50')


def calc_atr(df, period=14):
    """计算ATR（平均真实波幅）- 修复np.maximum bug"""
    if len(df) < period + 1:
        return 0.01
    
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    
    # 修复：np.maximum只接受两个参数，需要嵌套使用
    tr1 = high[1:] - low[1:]
    tr2 = np.abs(high[1:] - close[:-1])
    tr3 = np.abs(low[1:] - close[:-1])
    tr = np.maximum(np.maximum(tr1, tr2), tr3)
    
    atr = np.mean(tr[-period:])
    
    current_price = close[-1]
    return atr / current_price if current_price > 0 else 0.01


def calc_rsi(prices, period=14):
    """计算RSI"""
    if len(prices) < period + 1:
        return 50
    
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def check_rsi_divergence(close_prices, rsi_values, lookback=20):
    """检测RSI底背离：价格新低，RSI没新低"""
    if len(close_prices) < lookback or len(rsi_values) < lookback:
        return False
    
    # 找最近20天的最低点
    price_min_idx = np.argmin(close_prices[-lookback:])
    rsi_at_price_min = rsi_values[-lookback + price_min_idx]
    
    # 找最近20天的RSI最低点
    rsi_min_idx = np.argmin(rsi_values[-lookback:])
    price_at_rsi_min = close_prices[-lookback + rsi_min_idx]
    
    # 价格新低，但RSI没新低 = 底背离
    if close_prices[-1] < price_at_rsi_min and rsi_values[-1] > rsi_at_price_min:
        return True
    return False


def get_rsi_series_efficient(close_prices, period=14, max_lookback=60):
    """高效计算RSI序列（只计算最近max_lookback天）"""
    if len(close_prices) < period + 1:
        return [50] * len(close_prices)
    
    # 只计算最后max_lookback天，提高性能
    start_idx = max(0, len(close_prices) - max_lookback - period)
    relevant_prices = close_prices[start_idx:]
    
    rsi_series = []
    for i in range(period, len(relevant_prices)):
        window = relevant_prices[:i+1]
        rsi = calc_rsi(window, period)
        rsi_series.append(rsi)
    
    # 补齐前面的部分（用50填充）
    padding = len(close_prices) - len(rsi_series)
    return [50] * padding + rsi_series


def check_market_health(context):
    """检查大盘是否健康（沪深300）"""
    df_index = attribute_history('000300.XSHG', 20, '1d', ['close'], skip_paused=True)
    if df_index is None or len(df_index) < 20:
        return True
    
    index_close = df_index['close'].values
    index_ma10 = np.mean(index_close[-10:])
    index_ma20 = np.mean(index_close[-20:])
    
    # 大盘10日线 > 20日线，且价格在10日线上方
    is_healthy = index_close[-1] > index_ma10 > index_ma20
    return is_healthy


def calc_volatility(close_prices, period=20):
    """计算历史波动率（年化）"""
    if len(close_prices) < period + 1:
        return 0.2
    
    returns = np.diff(close_prices[-period-1:]) / close_prices[-period-1:-1]
    return np.std(returns) * np.sqrt(252)


def update_market_regime(context, price, ma200):
    """根据市场状态动态调整止盈止损参数（方向A）"""
    if price > ma200 * 1.15:      # 牛市
        g.current_take_profit = 0.30
        g.current_stop_loss = 0.05
        g.current_max_hold_days = 45
        regime = "牛市🚀"
    elif price > ma200 * 1.05:    # 中性
        g.current_take_profit = 0.20
        g.current_stop_loss = 0.035
        g.current_max_hold_days = 30
        regime = "中性⚖️"
    else:                          # 熊市/震荡
        g.current_take_profit = 0.15
        g.current_stop_loss = 0.03
        g.current_max_hold_days = 20
        regime = "熊市🐻"
    
    return regime


def trade(context):
    stock = g.stock
    
    # 获取当前价格
    df_price = attribute_history(stock, 1, '1d', ['close'], skip_paused=True)
    if df_price is None or len(df_price) == 0:
        return
    price = df_price['close'].iloc[-1]
    
    # 获取历史数据
    df = attribute_history(stock, 200, '1d', ['close', 'high', 'low', 'volume'], skip_paused=True)
    if df is None or len(df) < 60:
        return
    
    close_prices = df['close'].values
    volumes = df['volume'].values
    
    # ===== 技术指标计算 =====
    rsi = calc_rsi(close_prices)
    
    # 优化：高效计算RSI序列（只算最近60天）
    rsi_series = get_rsi_series_efficient(close_prices, 14, 60)
    
    ma20 = np.mean(close_prices[-20:])
    std20 = np.std(close_prices[-20:])
    bb_lower = ma20 - 2 * std20
    
    ma200 = np.mean(close_prices[-200:]) if len(close_prices) >= 200 else ma20
    ma_volume_20 = np.mean(volumes[-20:]) if len(volumes) >= 20 else volumes[-1]
    volume_ratio = volumes[-1] / ma_volume_20 if ma_volume_20 > 0 else 1.0
    
    # 趋势过滤：价格不能离200日均线太远
    can_trade = price > ma200 * 0.95
    
    # ===== 动态参数调整 =====
    atr_ratio = calc_atr(df, g.atr_period)
    dynamic_stop_loss = max(g.current_stop_loss, atr_ratio * 2)
    regime = update_market_regime(context, price, ma200)
    
    # ===== 信号评分系统 =====
    score = 0
    
    # 基础信号
    if rsi < g.rsi_buy:
        score += 1
    if price < bb_lower * g.bb_factor:
        score += 1
    if rsi < 30:
        score += 1
    
    # 方向B：成交量确认（缩量下跌是空头陷阱）
    if volume_ratio < 0.6 and price < bb_lower:
        score += 0.5
        log.info(f"缩量下跌(vol_ratio={volume_ratio:.2f})，空头陷阱加分")
    elif volume_ratio > 1.5 and price < bb_lower:
        score -= 1
        log.info(f"放量下跌(vol_ratio={volume_ratio:.2f})，真跌扣分")
    
    # 优化点1：RSI底背离
    if g.enable_divergence and len(rsi_series) > 20:
        if check_rsi_divergence(close_prices, np.array(rsi_series)):
            score += 1.5
            log.info("检测到底背离，加分1.5")
    
    # 优化点4：大盘环境过滤（熊市时降低仓位权重）
    market_healthy = check_market_health(context) if g.enable_market_filter else True
    
    # 优化点5：波动率过滤
    volatility = calc_volatility(close_prices) if g.enable_volatility_filter else 0.2
    
    log.info(f"price={price:.2f}, rsi={rsi:.1f}, regime={regime}, score={score}, "
             f"vol_ratio={volume_ratio:.2f}, vol={volatility:.1%}, market_healthy={market_healthy}")
    
    # 持仓状态更新
    if g.position == 1:
        g.hold_days += 1
        pnl = (price - g.entry_price) / g.entry_price
    
    # ===== 卖出逻辑 =====
    if g.position == 1:
        sell = False
        
        # 止损
        if pnl < -dynamic_stop_loss:
            sell = True
            log.info(f"止损: pnl={pnl:.2%} (动态止损{dynamic_stop_loss:.2%})")
        
        # 止盈
        elif pnl > g.current_take_profit:
            # 优化点3：分批止盈
            if g.enable_partial_profit and not g.partial_sold and pnl > 0.15 and pnl < g.current_take_profit:
                # 涨15%以上但还没到止盈点，卖1/3
                current_pos = context.portfolio.positions[stock].total_amount
                if current_pos > 0:
                    target_shares = int(current_pos * 0.66)  # 保留2/3，卖出1/3
                    order_target(stock, target_shares)
                    g.partial_sold = True
                    log.info(f"分批止盈1: pnl={pnl:.2%}, 减仓1/3, 剩余2/3")
            else:
                sell = True
                log.info(f"止盈: pnl={pnl:.2%}")
        
        # 优化点2：无进展止损（持仓一定天数后盈利太少）
        elif g.enable_time_stop and g.hold_days >= g.time_stop_days:
            if pnl < g.time_stop_min_pnl:
                sell = True
                log.info(f"无进展止损: 持仓{g.hold_days}天, pnl={pnl:.2%}")
        
        # 超时强制卖出
        elif g.hold_days > g.current_max_hold_days:
            sell = True
            log.info(f"超时: 持仓{g.hold_days}天 > {g.current_max_hold_days}天")
        
        if sell:
            order_target(stock, 0)
            g.position = 0
            g.entry_price = 0
            g.hold_days = 0
            g.partial_sold = False
            return
    
    # ===== 买入逻辑 =====
    if g.position == 0 and can_trade:
        if score >= 2:
            # 动态仓位：score>=3给70%，否则50%
            if score >= 3:
                position_pct = 0.7
            else:
                position_pct = 0.5
            
            # 大盘环境不佳，仓位减半
            if not market_healthy:
                position_pct *= 0.5
                log.info("大盘环境不佳，仓位减半")
            
            # 高波动环境，仓位降低
            if volatility > g.volatility_threshold:
                position_pct *= 0.7
                log.info(f"高波动环境({volatility:.1%})，仓位降至{position_pct:.0%}")
            
            target_value = context.portfolio.total_value * position_pct
            order_target_value(stock, target_value)
            g.position = 1
            g.entry_price = price
            g.hold_days = 0
            g.partial_sold = False
            log.info(f"买入: score={score}, pos={position_pct:.0%}, "
                    f"止盈={g.current_take_profit:.0%}, 止损={dynamic_stop_loss:.2%}")
    
    # ===== 记录每日收益率 =====
    if hasattr(context.portfolio, 'daily_return'):
        g.daily_returns.append(context.portfolio.daily_return)
    else:
        if len(g.daily_returns) > 0:
            prev_value = context.portfolio.previous_total_value
            curr_value = context.portfolio.total_value
            daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
            g.daily_returns.append(daily_return)
        else:
            g.daily_returns.append(0)


def backtest_compare(context):
    """回测对比：策略 vs 买入持有沪深300"""
    strategy_value = context.portfolio.total_value
    start_cash = context.portfolio.starting_cash
    
    df_bench = get_price('510300.XSHG', 
                         start_date=context.run_params.start_date,
                         end_date=context.current_dt.strftime('%Y-%m-%d'),
                         frequency='daily', 
                         fields=['close'])
    
    if df_bench is None or len(df_bench) == 0:
        return
    
    start_price = df_bench['close'].iloc[0]
    current_price = df_bench['close'].iloc[-1]
    buy_hold_value = start_cash * (current_price / start_price)
    
    strategy_return = (strategy_value / start_cash - 1) * 100
    bench_return = (buy_hold_value / start_cash - 1) * 100
    
    # 每周五输出
    if context.current_dt.weekday() == 4:
        log.info("=" * 60)
        log.info(f"【策略vs基准】日期: {context.current_dt.strftime('%Y-%m-%d')}")
        log.info(f"策略累计收益: {strategy_return:.2f}%")
        log.info(f"买入持有收益: {bench_return:.2f}%")
        
        diff = strategy_return - bench_return
        if diff > 0:
            log.info(f"✅ 策略跑赢基准 {diff:.2f} 个百分点")
        else:
            log.warn(f"⚠️ 策略跑输基准 {abs(diff):.2f} 个百分点")
        
        # 夏普比率（修复版）
        if len(g.daily_returns) >= 20:
            recent_daily_returns = g.daily_returns[-20:]
            if np.std(recent_daily_returns) > 0:
                sharpe = np.sqrt(252) * np.mean(recent_daily_returns) / np.std(recent_daily_returns)
                win_rate = sum(1 for r in recent_daily_returns if r > 0) / len(recent_daily_returns)
                log.info(f"近20日年化夏普: {sharpe:.2f}, 胜率: {win_rate:.1%}, 日均收益: {np.mean(recent_daily_returns):.3%}")
        
        log.info("=" * 60)