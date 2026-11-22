---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion
line: 7.c rejected
backtest: 023-03_flatter-range-stronger-reversion_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The farther a coin's daily close sits from the middle of its 30-day closing range, the more the coin keeps moving in that direction over the next 10 days, up from above the middle and down from below it.
Consequence: A trader should not fade moves away from the middle of a month's range, and can lean with them instead.
Why:
- F1: The market did the opposite of the idea: on the 5-day grid, the coin's 5-day return net of its drift, signed away from the middle of its 30-day range, was +0.61 % (t 2.91, n 2555). It was +0.30 % at 1 day (t 3.11), +0.50 % at 3 days (t 3.01), +1.26 % at 10 days (t 3.97, overlapping on the 5-day grid), and on a non-overlapping 10-day grid +1.09 % (t 2.53, n 1259). So moves away from the middle continued instead of reverting.
- F6: The 5-day continuation held on both sides: +0.63 % above the middle (t 1.99, n 1239) and +0.59 % below it (t 2.13, n 1316). A plain 30-day momentum sign gave a similar +0.54 % over 5 days (t 2.60) and +0.89 % over 10 days (t 2.80).
- F2: Flatness did not strengthen reversion and did not clearly change the continuation. At 10 days, the flatter half continued +1.37 % (t 2.47, n 629) and the less-flat half +0.80 % (t 1.22, n 630), with Welch t 0.67. At 5 days, the trendiest flatness quartile continued +0.24 % (t 0.48) against +0.69 % to +0.80 % (t 1.8 to 2.0) in the other three.
- F7: The tested reversion lost -0.40 % per case over 5 days (strength -0.039, 2912 cases), against a trade cost of 0.19 %. The opposite move, continuation, is about +0.61 % per case over 5 days and about +1.1 % over 10 days. That is roughly 3 to 6 times the cost.
