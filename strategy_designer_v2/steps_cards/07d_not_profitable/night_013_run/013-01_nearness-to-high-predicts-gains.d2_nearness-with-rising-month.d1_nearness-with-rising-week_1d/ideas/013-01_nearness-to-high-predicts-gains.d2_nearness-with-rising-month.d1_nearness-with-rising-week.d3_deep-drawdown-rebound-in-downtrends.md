---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the farther its daily close sits below its highest close of the past 52 weeks, the higher its return over the next 7 days.
Consequence: Use the bars this book now sits flat on, holding long in proportion to how deep a falling coin sits below its 52-week high.
Why:
- F1: The book earns a mean daily return of 0.000366 while the coins themselves average 0.001315, because the book is barely exposed: its mean position is 0.072, it is flat on 46% of bars and short on 21%, and long bars carry 99.8% of its gain (coin next-bar return 0.00295 when long, against 0.00053 when short and 0.00052 when flat).
- F5: Outside the trending regime the book holds almost nothing (mean position about -0.002), yet on its 7-day grid (790 cases) a lower closeness to the high predicts a higher excess 7-day return (slope -0.0105 per standard deviation, t -2.51), and so does a lower 30-day return (t -2.05).
