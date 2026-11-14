---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.g patterns
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a large one-day drop, a coin keeps drifting up over the following three days, not only the next one.
Consequence: A trader would hold rebound longs for several days instead of exiting after one bar.
Why:
- F6: The rebound lasts beyond one bar: non-overlapping 3-day returns after drops with z<−2 average +1.50%, with t=3.81 over 355 cases.
- F2: Where the bar closes within its range sorts what follows a drop. Drop days (z<−1.5) that close in the bottom fifth of their range are followed by +1.22%, with t=4.44 over 454 cases and 66.5% up. Drop days that close in the upper half are followed by −0.93%, with t=−1.23 over 45 cases and 44% up.
