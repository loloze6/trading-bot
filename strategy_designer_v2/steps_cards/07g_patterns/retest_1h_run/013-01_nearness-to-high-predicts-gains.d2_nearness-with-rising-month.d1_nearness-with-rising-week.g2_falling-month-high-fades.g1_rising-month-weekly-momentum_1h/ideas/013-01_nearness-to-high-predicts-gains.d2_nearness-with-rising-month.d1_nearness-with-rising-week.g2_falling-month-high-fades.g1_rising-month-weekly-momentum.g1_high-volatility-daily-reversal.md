---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the past 1 day, the higher its return over the next 1 day. The effect grows the higher the coin's 7-day volatility, and the largest rebounds follow the steepest falls when volatility is high.
Consequence: In a volatile coin, a sharp one-day drop is a reason to buy for the next day rather than sell, and a sharp one-day rise is a reason to trim.
Why:
- F1: A coin's 1-day return predicts its next 1-day return with the opposite sign, and only when its volatility is high. On the non-overlapping daily grid, the slope of the excess next-day return on the 1-day return is -0.1367 (t -11.09, n 5511) in each coin's top tercile of 7-day volatility. It is +0.0372 (t 2.13, n 5508) in the bottom tercile and +0.0157 (t 1.09, n 5507) in the middle one.
- F2: The 1-day reversal holds in every coin and almost every year. Pooled over all bars it is a slope of -0.0836 (t -10.97, n 17102). By coin, the slope runs from -0.064 (XRP, t -3.43) to -0.129 (XMR, t -6.93). By year, 7 of 8 slopes are negative, with t from -1.73 to -7.69; 2024 is the exception at +0.0075 (t 0.35).
- F3: The reversal shows mostly as a rebound after the worst days. In the bottom quintile of the 1-day return scaled by volatility, the next day's excess return is +0.41% (t 4.19, n 3306). The top quintile is -0.21% (t -2.39) and the middle quintiles sit near -0.1%.
