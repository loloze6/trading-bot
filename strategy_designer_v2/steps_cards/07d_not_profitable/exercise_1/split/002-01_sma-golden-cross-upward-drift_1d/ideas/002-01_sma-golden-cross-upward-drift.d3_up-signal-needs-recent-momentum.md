---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's short moving average is above its long one, the coin keeps rising only on days when its close is above its close of about a month earlier.
Consequence: A trader should hold the up-signal long only while the coin's recent one-month move is also up, and step aside when it has turned down.
Why:
- F9: Losses come from in-position days when the market has been falling over 20 days. These 5580 days average −0.42% for the book, against +0.87% on 4289 rising days. The in-position sample has more falling days than rising ones.
- F13: The book loses money in the bear years, with daily means of −0.00106 in 2018 and −0.00050 in 2022, despite being in position on only 25% and 36% of days. It trails the coin in every rising year, for example 0.00096 against 0.00423 in 2020.
- F10: In-position days in a newly started signal do poorly. Days 10–30 after the forecast turns on see the coin fall 0.00135 a day, against +0.0030 on days 30–60. This fits a cross that often fires near a short-lived peak before the trend sets in.
