---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close has stayed above its 200-day SMA for 60 to 120 days in a row, the coin keeps rising over the next 20 bars more than its usual drift.
Consequence: Enter a mature run above the long average rather than at the fresh cross.
Why:
- F7: The first 20 bars after the close moves above the SMA, which is the cross itself, underperform (mean excess -0.015, 40.8% hit, n 3030); bars 60 to 120 days into the run do better (mean +0.035, 45.6% hit, n 1315).
