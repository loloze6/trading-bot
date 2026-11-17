---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past 5 days relative to its past 30 days, the higher its return over the next 7 days.
Consequence: Thin recent volume is a reason to refuse a long, and rising participation a reason to take one.
Why:
- F7: Volume relative to its 20-day mean predicts 7-day excess returns overall: slope 0.00722, t = 2.52, n = 1958, with the lowest-volume quintile at -0.0157 (t = -3.10). The 5-day/30-day log volume ratio gives slope 0.01035, t = 3.34, n = 1678. Both are concentrated in 2024 and 2025 (t = 4.37 and 4.13 for the 20-day ratio) and in XRP and ZEC, and are flat or negative in most other years.
