---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 1 hour, measured in units of its own 20-day hourly volatility, the higher its return over the next 1 hour.
Consequence: A sharp one-hour drop is a reason to buy for a quick rebound over the following hour rather than to sell into it.
Why:
- F2: Falls within a single hour are partly bought back in the next hour, and the bigger the fall the bigger the rebound. After hours below -3 volatility units, the next hour averages +0.00125 (t 3.16, n 2930); after hours between -3 and -1.5 units, +0.00067 (t 5.47, n 14021). Among all falling hours the slope is -0.000349 (t -10.78, n 171063). Hourly rises show no matching reversal: -0.00017 (t -1.43) and -0.00014 (t -0.34).
