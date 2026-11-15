---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to its own 20-day volatility, the larger its return over the next 5 days.
Consequence: A trader would treat an unusually large up-day in a coin as a reason to buy or stay long for about a week, rather than to fade it.
Why:
- F3: On a non-overlapping 5-bar grid, after the day's return is in the highest quintile of its z-score against the prior 20-day volatility (mean z 1.54), the next 5-day excess return is +1.39% (t 2.88, n 529). The other four quintiles range from -0.57% to +0.32%, all with |t| below 1.2, so the effect sits in the largest up-shocks only.
