---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the closer its daily close sits to its highest close of the past 52 weeks, the lower its return over the next 7 days.
Consequence: In a falling month, a coin still near its yearly high is a candidate to lighten or short rather than buy.
Why:
- F4: While the 30-day return is negative (the strategy flat), a close nearer the 52-week high is followed by a lower 7-day return: rank slope t -3.74 on 258 cases. In the trending state the same slope is only -0.37 (n 300).
