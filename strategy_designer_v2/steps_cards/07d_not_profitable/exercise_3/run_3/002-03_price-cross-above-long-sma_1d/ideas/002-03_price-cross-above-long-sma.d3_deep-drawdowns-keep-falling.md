---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's close falls far below its recent high, price keeps falling over the following weeks, and the deeper the fall from that high, the larger the further decline.
Consequence: If confirmed, deep falls from a recent high are a reason to refuse longs, or to take a short, on that coin.
Why:
- F4: The book earns little when the coin is far below its recent high. In the bottom quintile of the 60-day drawdown (below -24.9 %) the mean bar gain is 0.00009 (t 0.25, n 1029), against 0.00355 (t 2.38, n 1029) in the top quintile (within 2.3 % of the high). On non-overlapping 20-bar samples with forecast > 0, the deepest quartile of the 60-day drawdown (below -17.3 %) is followed by a mean 20-bar return of -0.0631 (median -0.049, n 49). The other three quartiles are followed by +0.053 to +0.075.
