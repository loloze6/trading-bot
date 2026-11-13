---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.g patterns
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a down day of at least 1.5 times its 20-day volatility, in a coin that is volatile against its last 100 days and closes below its 100-day average, the next day's return is positive.
Consequence: Refuse to sell after a sharp down day in a volatile downtrend, and consider a one-day rebound long instead.
Why:
- F5: A large down day (move at or below -1.5 of 20-day volatility) is followed by a next-day rebound: +0.0044 (t 2.01, n 679, hit 61%). The rebound is concentrated in high-volatility bars below the 100-day average: +0.0133 (t 2.62, n 186, hit 64%). It is near zero in calm bars: -0.0022 (t -0.73, n 227).
