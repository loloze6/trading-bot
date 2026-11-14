---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the next-day rise is larger when the coin's recent 20-day volatility and 20-day return are high for that coin.
Consequence: A trader would size the trend long by how fast and how volatile the rise is, not by the gap between the averages.
Why:
- F5: Active-bar gains are concentrated in volatile and strongly rising states. Next-day book return is 0.37% in the highest-volatility tercile against 0.07% in the low and middle terciles, and 0.39% in the top 20-day-return tercile against 0.05% to 0.08% in the others.
- F3: A larger forecast does not earn more. Forward 10-bar return by forecast bucket is 1.46% (0-5), 1.67% (5-10), 0.81% (10-15) and 0.49% (15-20), then 2.38% at the cap. Over non-overlapping blocks the slope has t = 0.37.
