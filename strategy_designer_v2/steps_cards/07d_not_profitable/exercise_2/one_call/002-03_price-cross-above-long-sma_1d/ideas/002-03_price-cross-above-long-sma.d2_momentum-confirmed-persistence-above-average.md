---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin trading above its 200-day SMA keeps drifting up when its close is also higher than 20 bars ago, which shows the move is still being extended by late buyers.
Consequence: Hold the long only while 20-day momentum is positive, and refuse entries above the average after a 20-day decline.
Why:
- F1: Nearly all of the book's gain comes from active bars where both the 200-day SMA is rising (20-bar slope > 0) and 20-day momentum is positive: they summed +18.83 in daily book return over 3710 bars (mean +0.0051 a day), while active bars with a falling SMA and falling momentum summed −2.38 over 1916 bars (mean −0.0012 a day).
- F5: Being active while 20-day momentum is negative loses: those 4713 active bars averaged −0.00055 a day in book return, against +0.0040 for the 4746 active bars with positive momentum. With negative momentum, even forecasts of 12–20 lost (−0.0012 a day).
