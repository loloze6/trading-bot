---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A new 20-day closing high in a coin whose close is above its close of 50 days earlier is followed by a 10-day return above the coin's average. The drift belongs to breakouts inside an established uptrend.
Consequence: Take breakout longs only when the coin's 50-day trend is up, and refuse them in 50-day downtrends, where most of the bear-phase drawdown was taken.
Why:
- F4: Gains come from coins in a 50-day uptrend. When a coin was 50-day uptrending, its held days earned 0.00419 a day (t 3.86, n 4,258 coin-days). When it was 50-day downtrending, held days earned 0.00144 (t 0.82, n 1,935). Yet the book was still exposed 38% of the time in downtrends.
- F5: The breakout's drift is concentrated in uptrends. Over non-overlapping 10-bar periods, new 20-day highs beat the coin's all-window mean by 0.0367 when the coin's 50-day return was positive (t 2.65, n 200), against 0.0192 when it was negative (t 1.22, n 98). The overall figure is 0.0212 (t 2.45, n 446).
- F3: The losing periods are the bear phases. 2018 summed -1.41 and 2022 -0.55 in book daily returns, against coin-average sums of -1.26 and -0.67. Window w14 summed -1.01 with a -73% drawdown inside it, and w7 and w9 summed -0.51 and -0.56.
- F1: The book fails on its falls, not on its gain or its fees. Its chained maximum drawdown is -82.5% against about 0.62 a year of mean daily return (0.0017/day, sd 0.041, 2,898 book days). It is long-only and moves almost one-for-one with the market: mean +0.0234 on days the coins' average rose (1,551 days) and -0.0233 on days it fell (1,347 days).
