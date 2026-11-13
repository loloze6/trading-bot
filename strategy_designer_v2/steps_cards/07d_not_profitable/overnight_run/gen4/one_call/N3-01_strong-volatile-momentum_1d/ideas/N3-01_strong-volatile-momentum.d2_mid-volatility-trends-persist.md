---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.d not profitable
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day rise above a rising 60-day trend happens with mid-range rather than the highest 20-day volatility, the next 5 days rise more than the coin's average.
Consequence: A trader would take full-size longs in mid-range volatility and cut size when volatility is at its highest, where most of the losses sit.
Why:
- F7: Volatility shapes both gain and loss. In-position days in the high-volatility tercile hold the largest allocation (0.74) and carry 39% of all losing-day losses, with an annualised Sharpe of 0.75 against 1.11 in the mid tercile. At forecast ≥10, the excess 5-bar return is +2.0% in mid volatility (t=1.64, n=116), +0.9% in high volatility (t=0.88, n=163) and -0.5% in low volatility (n=43).
- F1: Fees do not explain the failure: the 1118 trades, all long, earn 5.64% each on average before fees and pay 0.10% in fees (t of gross = 3.43). The Calmar failure comes from drawdowns: the deepest book drawdown is -86% on ZECUSD, -71% on both LTCUSD and XRPUSD, and -86% in 2021.
