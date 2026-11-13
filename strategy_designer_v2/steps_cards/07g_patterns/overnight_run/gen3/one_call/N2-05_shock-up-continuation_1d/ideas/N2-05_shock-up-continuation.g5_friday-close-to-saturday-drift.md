---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's close-to-close return from Friday's UTC close to Saturday's UTC close is positive on average.
Consequence: A trader can time entries to Friday's close to capture the Saturday drift.
Why:
- F4: The next-day excess return depends on the weekday of the signal bar. After a Friday close it is +0.30% (t 3.76, 2479 coin-days) and after a Thursday close +0.25% (t 2.63, 2483). After a Monday close it is -0.24% (t -2.53, 2490) and after a Wednesday close -0.30% (t -2.70, 2489). These coin-days are pooled over six coins that move together, so the effective count is smaller.
