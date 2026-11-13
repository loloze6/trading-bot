---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that falls more than 1.5 times the coin's trailing 20-day standard deviation of daily returns, the next day's close is above that close more often than after ordinary days.
Consequence: A trader could refuse to sell into, or take a long after, a large one-day drop for a one-day rebound.
Why:
- F2: After a large down day the next day rises more often than usual: 58.6% of next-day excess returns are positive after a day below −2.5 trailing 20-day standard deviations (n=268, mean +0.66%, t=1.67), and 59.6% after a day between −2.5 and −1.5 (n=638, mean +0.33%, t=1.58), against 48.5% after ordinary days (n=12,145).
