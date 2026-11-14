---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When the coin's close is above its 200-day moving average, price keeps rising over the following bars, and further the farther the close sits above it. The rise is larger the closer the close sits to its recent high, and a close that has fallen far from that high while still above the long average is followed by further falls.
Consequence: A trader scales the long down as the coin's fall from its recent high deepens, instead of holding full size through a decline the long average has not yet registered.
Why:
- F1: The book fails on its falls. Its deepest fall over the daily returns chained in window order is -43.0 % against a yearly return of 16.6 % (Calmar 0.3855, needed 0.75). That fall is one episode across w15 to w17, where the reconstructed book lost 18.8 %, 8.4 % and 21.6 % over 67, 120 and 22 days.
- F2: Inside that episode every coin lost money for the book (summed gains -0.38 to -0.65). Each coin stood far below its 60-day high (mean dd60 -0.24 to -0.41) with its close at or below its 20-day SMA (mean distance 0.000 to -0.043). Its close was still mostly above the 200-day SMA (mean distance -8 to +21 %), so the forecast kept the book long through a short-term decline.
- F4: The book earns little when the coin is far below its recent high. In the bottom quintile of the 60-day drawdown (below -24.9 %) the mean bar gain is 0.00009 (t 0.25, n 1029), against 0.00355 (t 2.38, n 1029) in the top quintile (within 2.3 % of the high). On non-overlapping 20-bar samples with forecast > 0, the deepest quartile of the 60-day drawdown (below -17.3 %) is followed by a mean 20-bar return of -0.0631 (median -0.049, n 49). The other three quartiles are followed by +0.053 to +0.075.
