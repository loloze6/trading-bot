---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day move measured against its 30-day volatility, the more the coin moves back the other way over the next day, and this reversal is larger the higher the coin's 30-day volatility.
Consequence: After an outsized day in a volatile coin, a trader fades the move for one day instead of following it.
Why:
- F1: Across all coins, the next day's excess return falls as today's move grows: today's 1-day return divided by its 30-day volatility predicts the next day with slope -0.00184 per unit (t -4.46, 13,060 one-day cases), and the slope is negative in every coin (XMR -0.00466, t -4.93; ETH t -2.09; BTC t -1.74; LTC t -1.77).
- F2: This one-day reversal sits in the coin's most volatile stretches: slope -0.00531 (t -5.70, 4,355 cases) in each coin's highest tercile of 30-day volatility, -0.00125 (t -1.91) in the middle tercile and +0.00051 (t 0.96) in the lowest. After a 2-sigma day in the top tercile that is about 1 % back, against a 0.19 % trade cost.
- F3: The reversal is not steady over time: slope t of -3.68, -2.95 and -3.65 in 2018 to 2020 and -2.79 in 2023, but -0.79 and -0.57 in 2021 and 2022, and positive in 2024 and 2025 (+0.51, +0.37). When coins are averaged by date, the bins weaken (after a move below -2 sigma: +0.55 %, t 1.21), so part of the pooled t comes from coins moving together.
