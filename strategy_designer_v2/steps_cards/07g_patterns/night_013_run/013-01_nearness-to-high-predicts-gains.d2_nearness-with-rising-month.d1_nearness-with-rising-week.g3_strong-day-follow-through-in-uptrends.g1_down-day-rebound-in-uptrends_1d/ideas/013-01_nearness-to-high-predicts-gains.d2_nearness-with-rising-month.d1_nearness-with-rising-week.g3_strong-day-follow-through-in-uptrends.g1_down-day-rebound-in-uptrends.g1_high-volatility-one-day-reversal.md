---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 30-day daily volatility is high relative to its own usual level, the larger its latest one-day return in units of that volatility, the more its return over the next 1 day goes the opposite way, with falls followed by gains and rises followed by losses.
Consequence: In a volatile market, fade the day's move in proportion to its size rather than following it.
Why:
- F1: The coin's next-day excess return runs against the day's own volatility-scaled return only when 30-day volatility is high: the slope is -0.0058 (t -6.30, n 4355) in each coin's top volatility tercile, against -0.0013 (t -2.06) in the middle tercile and +0.0008 (t 1.46) in the low tercile. In the high tercile the slope is negative in all six coins (t from -0.90 for ZEC to -4.15 for XMR) and in both halves of the windows (w1-12: t -2.66, w13-24: t -5.79).
- F4: Up days in high volatility while the 30-day return is negative are followed by a weak next day, -0.0070 excess (t -4.46, n 1109), while high-volatility down days in the same regime are followed by +0.0068 (t 3.78, n 1200). The reversal of F1 is concentrated in falling months.
