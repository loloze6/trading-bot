---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.g patterns
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In each coin, the daily returns following Thursday and Friday UTC closes are higher than those following other weekdays' closes.
Consequence: A trader can time long entries for the Thursday close and hold through Saturday, and put off buying on Monday and Wednesday closes.
Why:
- F4: Returns after Thursday and Friday UTC closes are positive: +0.37% (t 3.89, n 2483) and +0.42% (t 5.23, n 2479). Returns after Monday and Wednesday closes are -0.12% and -0.18%. The Thursday/Friday effect is positive in all six coins (t 1.87–3.76) and in 7 of 8 years (t above 2 in 2019, 2020, 2023, 2024 and 2025). The book makes most of its money on those same days: +0.45% (t 3.90) and +0.47% (t 4.79) per day.
