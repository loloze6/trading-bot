---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-share-continuation
line: 7.g patterns
backtest: 010-02_rsi-below-share-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day return relative to its own 30-day volatility, the more its return over the next day runs the opposite way. The reversal grows as the coin's 30-day volatility rises.
Consequence: A trader can lean against a coin's unusually large daily moves for one day, most of all when the coin is volatile, and can refuse to chase them.
Why:
- F1: A coin's one-day move, scaled by its 30-day volatility, reverses on the next day, and the larger the move, the stronger the reversal. On every day's next-day excess return the Spearman is -0.073 (p = 0.000002, n = 4306). It holds in both coins: BTC -0.068 (slope t -1.96, n = 2153) and ETH -0.075 (slope t -2.44, n = 2153).
- F2: The next-day reversal is negative in every year from 2018 to 2025, 8 of 8. Spearman runs from -0.015 in 2022 to -0.151 in 2018, with about 538 days per year.
- F3: The reversal is about three times stronger when 30-day volatility is above its median. Spearman is BTC -0.095 and ETH -0.111 in that half, against -0.035 for both coins in the calmer half (about 1077 days in each cell).
- F4: The reversal is graded at the extremes. After a day below -2 standard deviations, the next day's excess return averages +0.83% (t 1.72, n 125). After a day above +2, it averages -0.59% (t -1.84, n 157). The middle bins sit near zero.
- F5: The reversal lasts one day only. Over the next 3 days on a non-overlapping grid the Spearman falls to -0.017 (p 0.52, n 1379). On the 3-day move scaled by volatility, the next 3 and 7 days turn slightly positive (0.021 and 0.028, p ≥ 0.44).
