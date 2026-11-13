---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is low against its own recent history and its 20-day return is positive, it drifts up over the next five days.
Consequence: A trader can take long exposure in calm, rising coins and refuse it in calm, falling ones.
Why:
- F5: When a coin's 20-day volatility is below 0.8 times its 120-day median and its 20-day return is positive, the next non-overlapping 5-bar excess return is +3.01% (t 2.48, 128 cases). Low volatility with a negative 20-day return gives -0.89% (t -1.03, 156 cases). Mid volatility gives +0.32% with a positive 20-day return and -0.80% with a negative one.
