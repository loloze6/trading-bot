---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In each coin, the daily bar that follows the Friday-stamped bar returns more than the coin's average daily bar, and the bar that follows the Wednesday-stamped bar returns less.
Consequence: Time entries so that longs are held over the post-Friday bar and are not opened ahead of the post-Wednesday bar.
Why:
- F4: The day after a Friday-stamped bar beat the coin's mean by 0.34%, t = 4.32, 54.5% up. This held in early windows (t = 4.31) and late windows (t = 2.00) and was positive in all six coins (t from 0.66 to 2.71). The day after a Wednesday-stamped bar was below the mean by 0.34%, t = -3.02, and negative in all six coins.
