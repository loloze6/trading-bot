---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose 200-day average itself has been rising over the past months earns more over the next 20 days while its close is above that average than a coin whose average is flat or falling.
Consequence: Take longs above the average only when the average is rising, which keeps the book out of the choppy crosses that cause its deep drawdowns.
Why:
- F8: Gains depend on the recent market direction.
- F9: The book is long only (share long 1.0) and has deep drawdowns, which explains the Calmar of 0.14.
- F5: Losses come from the first weeks of a trend, the noise around the cross.
