---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close is above its 200-day SMA keeps rising over the next weeks when that SMA has itself risen over the last 20 bars.
Consequence: Take long trend trades only above a rising 200-day SMA, and refuse them when the SMA is falling.
Why:
- F1: Nearly all of the book's gain comes from active bars where both the 200-day SMA is rising (20-bar slope > 0) and 20-day momentum is positive: they summed +18.83 in daily book return over 3710 bars (mean +0.0051 a day), while active bars with a falling SMA and falling momentum summed −2.38 over 1916 bars (mean −0.0012 a day).
- F2: Being above a falling 200-day SMA does not pay: active bars with a falling SMA averaged −0.00073 a day in book return and +0.8% over the next 20 bars, against +0.0029 a day and +5.1% when the SMA was rising; inside the falling-SMA group, the largest forecasts (12–20) did worst, at −0.0030 a day and −1.1% over 20 bars.
- F7: Losses cluster in years when the coin barely trends: in 2023 the book lost −0.00027 a day while the coin gained +0.0015 and the book was active 68% of the time; in 2018 and 2022 the book also lost (−0.0007 and −0.0004 a day).
