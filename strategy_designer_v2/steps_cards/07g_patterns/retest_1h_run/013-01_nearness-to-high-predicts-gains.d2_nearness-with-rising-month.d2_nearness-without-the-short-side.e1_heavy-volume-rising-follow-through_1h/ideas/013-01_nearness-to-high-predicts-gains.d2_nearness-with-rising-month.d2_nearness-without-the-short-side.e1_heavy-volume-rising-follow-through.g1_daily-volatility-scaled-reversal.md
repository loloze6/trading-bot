---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 1 day, measured in units of its own 20-day volatility, the higher its return over the next 1 day; the larger its rise, the lower that return.
Consequence: A coin that has just fallen hard over a day is a reason to be long for the next day, and one that has just surged is a reason to refuse a new long.
Why:
- F1: Past day's return predicts the next day in reverse, measured on the 24-hour grid with each return scaled by its own 20-day volatility. The weakest quintile is followed by a next-day excess return of +0.00472 (t 4.53, n 2874), and the strongest quintile by -0.00242 (t -2.57, n 2873). The pooled slope is -0.00237 (t -5.65, n 14366) and is negative in 6 of 8 years.
- F2: Falls within a single hour are partly bought back in the next hour, and the bigger the fall the bigger the rebound. After hours below -3 volatility units, the next hour averages +0.00125 (t 3.16, n 2930); after hours between -3 and -1.5 units, +0.00067 (t 5.47, n 14021). Among all falling hours the slope is -0.000349 (t -10.78, n 171063). Hourly rises show no matching reversal: -0.00017 (t -1.43) and -0.00014 (t -0.34).
