---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that rises more than 1.5 times the coin's trailing 20-day standard deviation of daily returns, the next day's close is below that close more often than after ordinary days.
Consequence: A trader could refuse to chase a new long on the close of a large up day.
Why:
- F3: After a large up day the next day rises less often than usual: 41.4% positive after a day above +2.5 standard deviations (n=319) and 44.9% after a day between +1.5 and +2.5 (n=691), against 48.5% after ordinary days, though the mean next-day excess is near zero (−0.08% and −0.03%).
