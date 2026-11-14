---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes with a daily rise that is large relative to its own recent volatility, the next day's close is lower on average.
Consequence: A trader should avoid buying the day after an outsized up day in a coin.
Why:
- F8: Large daily moves partly reverse the next day. After a drop of 2 standard deviations or more (n=366), the next day averaged +1.78% and the next 5 days +1.97%. After a rise of more than 2 standard deviations (n=495), the next day averaged −0.52%. After ordinary days (within ±1 sd), the next day averaged +0.05%.
