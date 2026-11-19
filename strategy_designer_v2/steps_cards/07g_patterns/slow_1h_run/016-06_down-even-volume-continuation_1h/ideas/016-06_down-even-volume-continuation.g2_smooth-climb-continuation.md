---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves that points in the direction of the rise, the more it keeps rising over the next 3 days.
Consequence: A smooth, steady climb is a reason to stay long, and a choppy climb of the same size a reason to step aside.
Why:
- F4: Among rising coins, the more efficient the 3-day climb, the more it continues over the next 72 hours. Efficiency here is the net hourly move over the sum of absolute hourly moves. The slope is +0.056 (t 3.30, 2865 cases), and the volatility-scaled 3-day return gives t 3.36. The efficiency slope is positive in all 6 coins and all 8 years.
