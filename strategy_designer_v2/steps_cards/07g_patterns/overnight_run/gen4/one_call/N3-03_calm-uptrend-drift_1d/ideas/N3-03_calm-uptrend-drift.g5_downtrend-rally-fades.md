---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.g patterns
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After an up day of at least 1.5 times its 20-day volatility in a coin closing below its 100-day average, the next day's return is negative.
Consequence: Refuse to chase a sharp up day while the coin is below its 100-day average.
Why:
- F6: A large up day (at or above +1.5 of 20-day volatility) with the close below the 100-day average is followed by a next-day excess of -0.0070 (t -2.04, n 224, hit 42%). Above the 100-day average the next day shows +0.0024 (t 0.76, n 396).
