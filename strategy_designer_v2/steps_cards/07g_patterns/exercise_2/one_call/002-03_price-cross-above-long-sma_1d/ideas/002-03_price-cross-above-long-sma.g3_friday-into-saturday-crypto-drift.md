---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's close-to-close return from Friday's daily close to Saturday's daily close is higher than its average daily return.
Consequence: A trader could prefer to hold a coin over the Friday-to-Saturday bar and avoid adding on Wednesday closes.
Why:
- F4: Next-day excess return depends on the weekday of the bar: after Friday bars it is +0.30% (t=3.66, 51.7% positive, n=2,430) and after Thursday bars +0.21% (t=2.29), while after Wednesday bars it is −0.30% (t=−2.75) and after Monday bars −0.22% (t=−2.34).
