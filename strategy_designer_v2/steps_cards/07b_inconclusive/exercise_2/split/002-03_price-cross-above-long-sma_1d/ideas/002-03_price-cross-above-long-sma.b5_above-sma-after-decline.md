---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day SMA but the coin has fallen over the trailing 60 days, the coin rises less than its usual drift over the next 20 bars.
Consequence: Refuse longs above the long average when the last 60 days were down.
Why:
- F8: Active bars whose coin fell over the trailing 60 days (bottom quartile, mean -7%) lose (mean excess -0.016, 32.6% hit); bars after a moderate +16% trailing rise do best (mean +0.058, 49.1% hit), and after a +115% rise the edge fades (mean +0.034, 42.8% hit).
- F2: On the 7046 active bars the typical outcome is a loss against holding: median 20-bar excess return -0.031 against a mean of +0.0065, standard deviation 0.298, maximum +4.57, and only 42.0% of bars beat the coin's drift.
