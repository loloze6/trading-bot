---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.g patterns
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rises on a day whose high-low range is much wider than its recent average tends to close lower the next day.
Consequence: A trader would avoid adding long exposure, or would trim, the day after a wide-range up day.
Why:
- F1: Across the six coins, a wide-range down day is followed by a next-day excess return of +0.89%, with t=6.07 over 1616 cases and 62.6% up days; a wide-range down day here means the top fifth of each coin's high-low range relative to its 60-day average. A wide-range up day is followed by −0.34%, with t=−2.04 over 1287 cases and 43.7% up days.
