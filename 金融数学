import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from arch import arch_model
from statsmodels.tsa.stattools import coint
import cvxpy as cp

# ================== 1. 随机过程模拟：GBM 和 OU ==================
print("=" * 60)
print("1. 随机过程模拟：几何布朗运动 (GBM) 与 奥恩斯坦-乌伦贝克 (OU)")
print("=" * 60)

np.random.seed(42)
T, n, dt = 1.0, 252, 1/252
paths = 5

# GBM 参数: dS = mu S dt + sigma S dW
mu, sigma, S0 = 0.05, 0.2, 100
gbm_paths = np.zeros((paths, n+1))
gbm_paths[:, 0] = S0
for i in range(paths):
    Z = np.random.standard_normal(n)
    for t in range(1, n+1):
        gbm_paths[i, t] = gbm_paths[i, t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z[t-1])

# OU 参数: dX = theta (mu - X) dt + sigma dW
theta, mu_ou, sigma_ou, X0 = 2.0, 1.0, 0.15, 2.0
ou_paths = np.zeros((paths, n+1))
ou_paths[:, 0] = X0
for i in range(paths):
    Z = np.random.standard_normal(n)
    for t in range(1, n+1):
        ou_paths[i, t] = ou_paths[i, t-1] + theta*(mu_ou - ou_paths[i, t-1])*dt + sigma_ou*np.sqrt(dt)*Z[t-1]

plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
for i in range(paths):
    plt.plot(np.linspace(0, T, n+1), gbm_paths[i], lw=1)
plt.title('Geometric Brownian Motion (GBM)')
plt.xlabel('Time (years)'), plt.ylabel('Price')
plt.subplot(1, 2, 2)
for i in range(paths):
    plt.plot(np.linspace(0, T, n+1), ou_paths[i], lw=1)
plt.title('Ornstein-Uhlenbeck (OU) Process')
plt.xlabel('Time (years)'), plt.ylabel('Value')
plt.tight_layout()
plt.show()

# GARCH 拟合 (使用模拟的收益率数据)
returns = 100 * (gbm_paths[0, 1:] / gbm_paths[0, :-1] - 1)
garch_model = arch_model(returns, vol='Garch', p=1, q=1, dist='normal')
garch_fit = garch_model.fit(disp='off')
print("\nGARCH(1,1) 模型拟合结果:")
print(garch_fit.summary())

# ================== 2. 欧式期权定价：蒙特卡洛 vs Black-Scholes ==================
print("\n" + "=" * 60)
print("2. 欧式看涨期权定价：蒙特卡洛模拟 vs Black-Scholes 公式")
print("=" * 60)

# 参数: S0, K, T, r, sigma
S0, K, T, r, sigma = 100, 105, 1.0, 0.05, 0.2
M, N_sim = 252, 100000
dt = T / M

# 蒙特卡洛模拟 (10行代码实现)
np.random.seed(42)
Z = np.random.standard_normal((N_sim, M))
ST = S0 * np.exp(np.cumsum((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z, axis=1))[:, -1]
call_mc = np.exp(-r*T) * np.mean(np.maximum(ST - K, 0))

# Black-Scholes 公式
def black_scholes_call(S0, K, T, r, sigma):
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S0 * stats.norm.cdf(d1) - K * np.exp(-r*T) * stats.norm.cdf(d2)

call_bs = black_scholes_call(S0, K, T, r, sigma)
print(f"蒙特卡洛价格: {call_mc:.4f}")
print(f"Black-Scholes价格: {call_bs:.4f}")
print(f"相对误差: {abs(call_mc - call_bs)/call_bs*100:.2f}%")

# ================== 3. 配对交易：协整检验与回测 ==================
print("\n" + "=" * 60)
print("3. 配对交易：协整检验 (使用模拟相关价格序列)")
print("=" * 60)

# 模拟两只高相关性股票价格 (协整关系: y = beta * x + spread)
np.random.seed(42)
T_days = 1000
x = np.cumsum(np.random.normal(0, 1, T_days)) + 100
beta = 0.85
spread = np.random.normal(0, 2, T_days).cumsum() * 0.1  # 均值回复价差
y = beta * x + spread
prices = pd.DataFrame({'Stock_A': x, 'Stock_B': y})

# 协整检验
score, pvalue, _ = coint(prices['Stock_A'], prices['Stock_B'])
print(f"协整检验 p值: {pvalue:.4f}")
print("存在协整关系" if pvalue < 0.05 else "不存在协整关系")

# 简单回测: 计算价差 z-score 并生成交易信号
spread_series = prices['Stock_A'] - beta * prices['Stock_B']
zscore = (spread_series - spread_series.mean()) / spread_series.std()
entry_threshold, exit_threshold = 1.5, 0.5
position = np.zeros(T_days)
position[zscore > entry_threshold] = -1   # 做空价差 (卖A买B)
position[zscore < -entry_threshold] = 1   # 做多价差 (买A卖B)
# 退出条件
position[np.abs(zscore) < exit_threshold] = 0
position = pd.Series(position).fillna(method='ffill').fillna(0).values

# 计算策略收益
returns_A = prices['Stock_A'].pct_change().fillna(0).values
returns_B = prices['Stock_B'].pct_change().fillna(0).values
strategy_returns = position * (returns_A - beta * returns_B)  # 简化收益计算
sharpe_ratio = np.sqrt(252) * strategy_returns.mean() / strategy_returns.std() if strategy_returns.std() > 0 else 0

print(f"策略年化夏普比率: {sharpe_ratio:.3f}")

# ================== 4. 美式期权定价：最小二乘蒙特卡洛 (LSM) ==================
print("\n" + "=" * 60)
print("4. 美式看跌期权定价：最小二乘蒙特卡洛 (LSM)")
print("=" * 60)

def LSM_put(S0, K, T, r, sigma, n_steps, n_paths, deg=3):
    """最小二乘蒙特卡洛美式看跌期权定价"""
    dt = T / n_steps
    discount = np.exp(-r * dt)

    # 模拟价格路径
    np.random.seed(42)
    Z = np.random.standard_normal((n_paths, n_steps))
    S = np.zeros((n_paths, n_steps + 1))
    S[:, 0] = S0
    for t in range(1, n_steps + 1):
        S[:, t] = S[:, t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z[:, t-1])

    # 现金流矩阵 (行权收益)
    cashflow = np.maximum(K - S[:, -1], 0)

    # 逆向递推
    for t in range(n_steps - 1, 0, -1):
        in_the_money = S[:, t] < K
        if not np.any(in_the_money):
            continue
        X = S[in_the_money, t]
        Y = cashflow[in_the_money] * discount
        # 多项式回归拟合继续价值
        coeffs = np.polyfit(X, Y, deg)
        continuation_value = np.polyval(coeffs, X)
        exercise_value = K - X
        # 行权决策
        exercise = exercise_value > continuation_value
        cashflow[in_the_money][exercise] = exercise_value[exercise]
        cashflow[in_the_money][~exercise] = Y[~exercise] / discount  # 继续持有

    return np.mean(cashflow * np.exp(-r * dt))

S0, K, T, r, sigma = 100, 105, 1.0, 0.05, 0.2
# 欧式看跌期权作为比较基准
d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2 = d1 - sigma*np.sqrt(T)
put_eu = K * np.exp(-r*T) * stats.norm.cdf(-d2) - S0 * stats.norm.cdf(-d1)

put_am = LSM_put(S0, K, T, r, sigma, n_steps=50, n_paths=50000, deg=3)
print(f"欧式看跌期权价格: {put_eu:.4f}")
print(f"美式看跌期权价格 (LSM): {put_am:.4f}")
print(f"美式溢价: {(put_am - put_eu)/put_eu*100:.2f}%")
print("注: 美式期权价格应 >= 欧式期权价格，LSM 是近似算法")

# ================== 5. 投资组合优化：cvxpy 凸优化 ==================
print("\n" + "=" * 60)
print("5. 投资组合优化：最小方差组合 (cvxpy)")
print("=" * 60)

np.random.seed(42)
n_assets = 5
returns_assets = np.random.normal(0.0005, 0.02, (n_assets, 1000))
cov_matrix = np.cov(returns_assets)
mu = np.mean(returns_assets, axis=1)

# 使用 cvxpy 求解最小方差组合
w = cp.Variable(n_assets)
portfolio_variance = cp.quad_form(w, cp.psd_wrap(cov_matrix))
constraints = [cp.sum(w) == 1, w >= 0]  # 权重和为1，不允许卖空
objective = cp.Minimize(portfolio_variance)
problem = cp.Problem(objective, constraints)
problem.solve()

print(f"优化状态: {problem.status}")
print("最优权重:", w.value.round(4))
print(f"组合年化波动率: {np.sqrt(portfolio_variance.value) * np.sqrt(252):.2%}")
