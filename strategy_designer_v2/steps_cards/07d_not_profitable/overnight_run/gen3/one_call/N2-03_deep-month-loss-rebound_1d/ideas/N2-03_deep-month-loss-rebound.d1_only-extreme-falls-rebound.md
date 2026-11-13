---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.d not profitable
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 20-day fall is followed by further decline when the fall is only mild relative to its recent 20-day moves. Only a fall that is extreme against those recent moves is followed by an above-usual rise over the next 20 days.
Consequence: Refuse long entries on ordinary 20-day declines and buy only the extreme ones, holding toward a 20-day horizon rather than reacting to day-to-day forecast changes.
Why:
- F4: Small forecasts lose and deep ones gain. Over non-overlapping 20-bar periods, forecasts between 0 and 2 are followed by -4.36% excess return (t -2.63, n=167), while forecasts of 5 or more are followed by +3.11% (t 2.06, n=216). The two lower forecast quartiles show -3.7% and -3.9% (t about -1.8 to -1.9, n=105 each).
- F5: The deep-fall rebound needs time. The excess return after forecasts of 5 or more rises with the horizon: +0.19% at 5 bars (t 0.50, n=814), +0.77% at 10 bars (t 1.11, n=414) and +3.11% at 20 bars (t 2.06, n=216).
- F1: Fees are not why the book fails. Across 3297 trades, all long, the mean gross gain is -0.51% against a mean fee of 0.10%, so the trades already lose before costs.
