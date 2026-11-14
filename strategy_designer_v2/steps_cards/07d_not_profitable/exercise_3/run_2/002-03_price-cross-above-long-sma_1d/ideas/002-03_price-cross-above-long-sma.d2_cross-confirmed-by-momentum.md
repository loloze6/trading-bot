---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its long moving average, it keeps drifting upward further the further it sits above, only while the coin's own return over the past few months is positive, and the drift grows with that return.
Consequence: A trader refuses longs above the average when the coin is still down over recent months, which cuts the held days that lose steadily.
Why:
- F3: Held days after a non-positive 60-day return lost -0.000623 a day (n=1473, t -2.35). Held days after a positive 60-day return gained 0.001948, 0.003423 and 0.010923 across rising bands of that return (n=1698, 1499, 397).
- F5: Fresh crosses do not pay. Blocks within 20 days of the forecast turning on returned -0.021 excess (n=162, t -1.21), and the lowest forecast bin (0 to 5) returned -0.029 (n=111, t -1.63).
