---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 14-day return scaled by its 20-day volatility is followed by a move in the same direction over the next 7 days, larger the larger that scaled return.
Consequence: Over a one-week horizon, side with the coin's two-week trend rather than fade it.
Why:
- F4: Over longer spans, moves continue rather than reverse: on the non-overlapping 7-day grid, the 14-day volatility-scaled return predicts the next 7-day excess return with slope 0.01213 (t 4.40, n 2011), and the 7-day return gives slope 0.01024 (t 3.67), led by XRP (t 2.87) and ZEC (t 2.36); the slope drops to t 0.56 once each window's own mean is removed, so it reads as persistence of trends lasting several weeks.
