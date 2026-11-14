---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.g patterns
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is low against its last 100 days and whose 20-day return is positive, the next five days drift up when the close is also above its 100-day average and the 60-day return is positive.
Consequence: Take calm-uptrend longs only when the longer trend agrees, and refuse them when the 60-day return is negative.
Why:
- F1: Among non-overlapping 5-bar long cases, the calm-uptrend drift appears only when the longer trend is also up: long bars with a positive 60-day return show a mean excess of +0.0153 (t 2.38, n 276, hit 55%), against +0.0011 (t 0.28, n 621) when the 60-day return is not positive. In calm bars, closes above the 100-day average with a positive 60-day return give +0.0125 (t 2.07, n 300), while closes above the 100-day average with a negative 60-day return give -0.0344 (t -2.79, n 34).
- F2: The active-bar edge depends on the year: excess 5-bar returns are +0.0337 in 2020 (t 4.98, n 145) and +0.0293 in 2021 (t 2.51, n 138), but -0.0322 in 2018 (t -2.45, n 74) and -0.0275 in 2022 (t -3.19, n 114). The other years sit near zero (|t| < 0.9).
