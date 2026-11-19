---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day volatility relative to its 30-day volatility, the larger the reversal of its 1-day return over the next 1 day.
Consequence: When a coin's short-term volatility jumps above its usual level, fade its latest day's move for the next day.
Why:
- F1: A coin's 1-day return predicts its next 1-day return with the opposite sign, and only when its volatility is high. On the non-overlapping daily grid, the slope of the excess next-day return on the 1-day return is -0.1367 (t -11.09, n 5511) in each coin's top tercile of 7-day volatility. It is +0.0372 (t 2.13, n 5508) in the bottom tercile and +0.0157 (t 1.09, n 5507) in the middle one.
- F2: The 1-day reversal holds in every coin and almost every year. Pooled over all bars it is a slope of -0.0836 (t -10.97, n 17102). By coin, the slope runs from -0.064 (XRP, t -3.43) to -0.129 (XMR, t -6.93). By year, 7 of 8 slopes are negative, with t from -1.73 to -7.69; 2024 is the exception at +0.0075 (t 0.35).
