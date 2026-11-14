---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-01_weekday-of-coming-bar
line: 7.g patterns
backtest: N2-01_weekday-of-coming-bar_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily bar closes in the lowest part of its high-low range, the next daily bar returns more than the coin's average day.
Consequence: A trader would prefer long entries after bars that close near their low, and avoid chasing bars that close near their high.
Why:
- F3: Where the bar closes within its range orders the next bar's excess return almost monotonically. A close in the bottom fifth gives +0.0038 (t 3.80, n 2631); a close in the top fifth gives -0.0021 (t -2.64, n 3716). A z ≤ -1 down bar that also closes in the bottom fifth gives +0.0079 (t 4.54, n 944).
- F1: After a down bar that falls more than one 20-bar standard deviation, the next bar beats the coin's mean daily return: +0.0048 (t 3.29, n 1302) for z in (-2,-1] and +0.0069 (t 2.58, n 476) for z ≤ -2. After a small up bar (z in (0,1]) the next bar lags the mean by -0.0021 (t -3.36, n 5275), and all six coins show that lag.
