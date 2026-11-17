---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 1 day.
Consequence: Do not chase a coin lower after a sharp down day in a falling month, because the next day tends to bounce.
Why:
- F3: The rebound after vol-scaled falls is at least as strong when the 30-day return is negative. Falls beyond 2 daily volatilities return +0.0083 (t 1.97, n 255) and falls of 1 to 2 volatilities return +0.0045 (t 2.27, n 681). The per-coin slope of the next-day return on fall size is positive in all six coins in that regime (t 0.53 to 2.66), against five of six while the 30-day return is positive.
- F4: Up days in high volatility while the 30-day return is negative are followed by a weak next day, -0.0070 excess (t -4.46, n 1109), while high-volatility down days in the same regime are followed by +0.0068 (t 3.78, n 1200). The reversal of F1 is concentrated in falling months.
