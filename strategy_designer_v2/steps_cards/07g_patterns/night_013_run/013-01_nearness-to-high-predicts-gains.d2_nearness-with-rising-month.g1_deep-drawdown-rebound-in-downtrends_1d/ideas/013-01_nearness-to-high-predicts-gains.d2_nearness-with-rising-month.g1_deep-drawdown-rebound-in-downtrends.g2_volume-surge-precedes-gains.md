---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days.
Consequence: A rise in volume would favour holding a coin long over the next week, and unusually thin volume would be a reason to stay out.
Why:
- F4: A coin's volume relative to its 20-day average (log) predicts its 7-day forward excess return with slope 0.0125 (t 2.64, n 2011). The lowest-volume fifth averages -0.0124 (t -2.32), but the effect is carried mostly by ZEC (t 2.21) and XRP (t 1.75); in BTC, ETH, LTC and XMR the t lies between -0.1 and 1.0.
