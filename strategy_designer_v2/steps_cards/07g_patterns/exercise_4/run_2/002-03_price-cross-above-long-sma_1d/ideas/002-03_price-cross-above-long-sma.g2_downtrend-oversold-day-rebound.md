---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day average, the larger its one-day fall relative to its past 20-day daily volatility, the larger its rise above its average return over the next day.
Consequence: In a coin's downtrend, oversold one-day drops are the best short-term buying points, and trend-following exits taken on such a day give up a graded rebound.
Why:
- F1: A coin's next-day excess return falls steadily as its one-day move, scaled by its prior 20-day volatility, rises. The bottom decile of scaled moves is followed by +0.55% (t=3.67, n=1378, hit 58.5%) and the second decile by +0.26% (t=2.08). Deciles 3 to 9 are flat to negative (−0.22% at decile 7, t=−1.91). The regression slope of the next-day return on the scaled move is −0.0014 (p=0.00008, about 9,600 bars).
- F3: The rebound after the bottom two deciles of scaled falls is larger when the close is below its 200-day SMA (+0.54%, t=4.13, n=1543) than above it (+0.24%, t=1.61, n=1213). A 3-day version on the non-overlapping 3-day grid still shows +0.86% after bottom-decile falls (t=2.08, n=452).
