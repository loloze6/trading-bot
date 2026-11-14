---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day SMA and the coin has risen moderately over the trailing 60 days (around +10% to +30%), the coin keeps rising over the next 20 bars more than its usual drift.
Consequence: Take the above-average long only when the recent 60-day rise is moderate, not when it is negative or already extreme.
Why:
- F8: Active bars whose coin fell over the trailing 60 days (bottom quartile, mean -7%) lose (mean excess -0.016, 32.6% hit); bars after a moderate +16% trailing rise do best (mean +0.058, 49.1% hit), and after a +115% rise the edge fades (mean +0.034, 42.8% hit).
