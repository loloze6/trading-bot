---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return from Wednesday's close to Thursday's close is below its average daily return.
Consequence: A trader should avoid opening longs at Wednesday's close and should defer purchases by a day.
Why:
- F4: Wednesday closes are followed by a below-average next day (excess -0.30%, n=2437, t=-2.75, 45.2% positive), and this is negative in all six coins (-0.14% to -0.40%).
