---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes down by more than about three times its trailing 20-day mean absolute daily return, its price keeps falling over the next five days.
Consequence: A trader should not buy the dip after an extreme down day; it is a moment to stay out or reduce.
Why:
- F2: Very large down days, below -3 times the trailing scale, are followed by a further 5-bar excess return of -1.35% (t -2.18, 252 de-duplicated events). Down days between -3 and -2 show no such continuation (+0.53%, t 1.09, 419 events).
