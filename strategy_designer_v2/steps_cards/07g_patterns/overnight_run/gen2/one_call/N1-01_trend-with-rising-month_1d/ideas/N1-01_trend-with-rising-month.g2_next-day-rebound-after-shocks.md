---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.g patterns
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's daily close falls by more than about one and a half times its trailing 20-day volatility, its next daily return is positive more than usual, in both up- and down-trends.
Consequence: A trend-follower should not exit, and a trader may buy, on the close of a sharp down day, because the following day tends to recover part of it.
Why:
- F4: After a day that falls more than 1.5 times its trailing 20-day volatility, the next day returns +0.45% to +0.78% (n=636, t=2.17 and n=267, t=1.97), against +0.11% after ordinary days. The rebound is the same whether the 20-day trend is up or down (+0.54%, t=1.84 and +0.56%, t=2.32). It is largest after sharp drops on the Thursday-stamped bar (+1.59%, n=155, t=3.63) and in XMR (+1.19%, n=162, t=3.20).
