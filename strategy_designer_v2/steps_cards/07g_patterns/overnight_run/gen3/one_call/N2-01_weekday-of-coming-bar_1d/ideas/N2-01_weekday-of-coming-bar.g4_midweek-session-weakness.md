---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-01_weekday-of-coming-bar
line: 7.g patterns
backtest: N2-01_weekday-of-coming-bar_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Tuesday and Thursday daily sessions return less than its average day.
Consequence: A trader would stay out of or trim long exposure going into Tuesday and Thursday sessions.
Why:
- F4: Weekday sessions differ from each other, and Saturday is not the only one that stands out. Saturday is +0.0034 (t 4.07, n 2467) and Friday is +0.0021 (t 2.23, n 2462). Tuesday is -0.0025 (t -2.60, n 2472), negative in 5 of 6 coins. Thursday is -0.0030 (t -2.69, n 2472), negative in all 6 coins, but 2019 alone carries t -6.99 (n 312).
