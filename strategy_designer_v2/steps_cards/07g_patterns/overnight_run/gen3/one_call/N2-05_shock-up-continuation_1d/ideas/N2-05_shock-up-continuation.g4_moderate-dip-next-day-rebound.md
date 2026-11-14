---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes down by between one and two times its trailing 20-day mean absolute daily return, it rises the next day.
Consequence: A trader can buy at the close of a moderate down day for a one-day rebound.
Why:
- F3: Moderate down days, between -2 and -1 times the trailing scale, are followed by a next-day excess return of +0.60% (t 4.10, 1020 de-duplicated events). Flat days (-1 to 1) show -0.11% (t -1.09, 2004 events).
