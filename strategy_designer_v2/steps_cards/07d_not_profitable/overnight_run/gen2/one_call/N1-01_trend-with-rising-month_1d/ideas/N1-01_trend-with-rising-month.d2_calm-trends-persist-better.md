---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.d not profitable
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin above its rising long average drifts upward over the next 20 bars more when its recent 20-day volatility is low relative to its own history.
Consequence: Refuse or shrink trend longs when the coin's recent daily swings are in its high range, since they add drawdown without adding drift.
Why:
- F1: The book fails on drawdown, not on fees. Calmar is 0.50, below the 0.75 required. Each coin's worst drawdown runs from -46% (BTC) to -70% (ZEC, XRP), and the mean drawdown per window is -23.7%. Over 2,285 trades, fees average 0.10% against a mean gross gain of 5.19%, and the total fees paid (234) are 2% of the total gross gain (11,857).
- F6: Volatile states add drawdown without adding drift.
