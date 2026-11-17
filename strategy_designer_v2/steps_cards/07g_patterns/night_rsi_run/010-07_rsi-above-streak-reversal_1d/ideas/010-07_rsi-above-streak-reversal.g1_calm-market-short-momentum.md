---
brief: 010_rsi-midline-regime-direction
source-idea: 010-07_rsi-above-streak-reversal
line: 7.g patterns
backtest: 010-07_rsi-above-streak-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, the lower its 20-day volatility of daily returns, the more its 3-day return continues in the same direction over the next 3 days.
Consequence: In quiet markets a trader can follow the last few days' move, and should refuse to chase short moves when volatility is high.
Why:
- F4: Short-term momentum is concentrated in calm markets. On a non-overlapping 3-day grid, the slope of the next 3-day return on the past 3-day return is 0.211 (t = 3.72, n = 524) in the lowest 20-day-volatility tercile. In the middle tercile it is 0.009 (t = 0.20), and in the highest it is −0.025 (t = −0.66).
- F5: The calm-market momentum has the same sign in every split I made. The low-volatility slope is 0.257 (t = 3.45) in ETH and 0.100 (t = 1.07) in BTC, and 0.155 (t = 1.91) in w1–w12 and 0.270 (t = 3.41) in w13–w24. A graded version, the vol-scaled 3-day return weighted by how low the volatility is, gives t = 2.59 (n = 1571). At 7 days the gradient is weaker: the low-volatility slope is 0.091 (t = 1.01) against −0.019 (t = −0.32) in the high-volatility tercile.
