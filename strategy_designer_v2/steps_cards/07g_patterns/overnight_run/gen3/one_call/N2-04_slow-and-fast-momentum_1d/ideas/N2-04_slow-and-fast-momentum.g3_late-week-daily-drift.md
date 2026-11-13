---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the day after a weekday-4 bar is higher than its return after the other weekdays' bars.
Consequence: A long holder should prefer to be in the market over that day and to delay exits until after it.
Why:
- F6: The next-day return following a weekday-4 bar was +0.37% when averaged across coins per day (t = 2.31, 345 days). Weekday-3 and weekday-4 bars together beat the other weekdays in 5 of 6 coins and 6 of 8 years. This is the strongest of 7 weekdays tested, so it is weaker evidence than F1.
