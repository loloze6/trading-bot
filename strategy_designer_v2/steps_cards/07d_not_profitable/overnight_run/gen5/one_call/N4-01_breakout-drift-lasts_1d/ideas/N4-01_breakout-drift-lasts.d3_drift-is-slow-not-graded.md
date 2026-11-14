---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Once a new 20-day high has been made, the upward drift of the following weeks accrues evenly across the days of the hold and does not grow with how close the latest close is to the high.
Consequence: Hold a fixed-size long through the weeks after the high instead of scaling it up near the high, which cuts drawdown without giving up drift.
Why:
- F3: A larger forecast earns more only on the next day, and not over ten days. The next-day return rises from -0.0002 in the lowest active forecast fifth to +0.0028 and +0.0025 in the top two. On non-overlapping 10-bar returns of active bars, the forecast buckets 0-8, 8-15 and 15-20 give +1.6%, -1.2% and +0.4% (t 0.76, -0.89, 0.28; n = 36, 58, 56). Over all 198 such cases the mean is -0.1% (t -0.11).
- F4: Position grows with the forecast to an average of 1.97 at forecast 20, against 0.35 at forecasts up to 5, so the book is near 2x long exactly where F3 shows no 10-bar edge. This leverage adds to the drawdowns in F1.
- F2: The gains are lopsided by holding time. The 1705 trades held more than 15 days earn +12.0% gross each (sum of net +20336%). The 1563 trades held 15 days or less all lose on average: -9.1% for 1 day or less, -4.6% for 1.5 to 3.5 days, -4.4% for 3.5 to 7.5 days and -3.3% for 7.5 to 15 days (sum of net -6374%). Overall the median trade is -2.4% and only 41.7% of trades win.
- F1: Fees are not the cause: the book is long only with 3269 trades, a mean gross gain of 4.37% per trade (t 5.72 over 3269 trades) against a mean commission of 0.29%, so the net mean is still 4.27%. The failed check is Calmar at 0.44, driven by drawdowns: the worst window drawdown per coin ranges from -73% (BTC) to -86% (LTC), and the window-mean drawdown reaches -77% in w14.
