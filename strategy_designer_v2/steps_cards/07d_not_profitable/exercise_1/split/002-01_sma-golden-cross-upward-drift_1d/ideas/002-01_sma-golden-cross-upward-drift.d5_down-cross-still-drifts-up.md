---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's short moving average crosses below its long one, the coin's price still drifts upward on average.
Consequence: A trader should keep a baseline long rather than go flat on a down-cross, and use the up-signal only to adjust around that baseline.
Why:
- F3: On days in a position the book makes 0.00141 a day while the coin makes 0.00149. The forecast therefore adds nothing over holding when it is on. On flat days the coin still rises 0.00100 a day and the book makes about 0.
- F1: The book earns less per unit of risk than holding: its daily Sharpe is 0.306 against the coin's 0.509, and its daily return sd is 0.0510 against the coin's 0.0483, even though it is in a position on only 9869 of 17022 days.
- F13: The book loses money in the bear years, with daily means of −0.00106 in 2018 and −0.00050 in 2022, despite being in position on only 25% and 36% of days. It trails the coin in every rising year, for example 0.00096 against 0.00423 in 2020.
