---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin trades above its 200-day average, the lower its 60-day volatility, the larger its average daily return over the next day.
Consequence: A trader following a coin's trend above its long average would hold it with more conviction in calm stretches and expect little from the trend in volatile ones.
Why:
- F2: On days the book is long, the position's next-day gain is 0.00364 per bar (t 3.93, n 1689) in the coin's lowest tercile of 60-day volatility, against 0.00028 (t 0.40) and 0.00041 (t 0.72) in the middle and highest terciles. The trend above the 200-day average pays almost only when the coin is calm.
- F5: The book's gain comes from a few long trends. Trades in the longest duration quartile (mean 63 days) average +35.7% with 68.7% winners, while the shortest quartile (1.8 days) averages -5.8% with 3% winners. The book's mean bar gain of 0.000580 is mostly the market's own rise, 0.000342, rather than timing, 0.000238.
