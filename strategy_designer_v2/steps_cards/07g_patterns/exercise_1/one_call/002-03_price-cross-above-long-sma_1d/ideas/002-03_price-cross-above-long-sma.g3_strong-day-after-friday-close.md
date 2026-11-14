---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return from Friday's close to Saturday's close is above its average daily return.
Consequence: A trader should prefer to hold or open longs at Friday's close rather than at other closes.
Why:
- F5: Friday closes are followed by an above-average next day (excess +0.30%, n=2430, t=3.66, 51.7% positive), positive in all six coins; Thursday is also positive (+0.21%, t=2.29, positive in all six coins), while Monday is negative (-0.22%, t=-2.34, negative in 5 of 6 coins).
