---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the coin keeps rising, further the larger the spread, except in the early stretch just after the cross; the drift grows with the time the short average has stayed above the long one.
Consequence: A trader would scale into a golden-cross long as the cross ages, rather than buying the fresh cross.
Why:
- F1: The bars just after the forecast turns positive lose money: in the first 20 days of a long stretch the book's mean daily return is -0.000512 (Sharpe -0.34, n=2065) and the coin's is -0.000471, against 0.000993 for days 20–60 (n=3524) and 0.001657 for days 60–120 (n=2619, Sharpe 0.90); the weak forecast bucket 0–5 also earns -0.000011 a day (n=2154).
