---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past hour, the more its return over the next hour exceeds its average hourly return.
Consequence: A trader can delay selling, or add to a long, right after a sharp hourly drop, because the next hour tends to recover part of the fall.
Why:
- F4: The reversal also shows at the hourly scale: after the lowest quintile of one-hour returns, the next hour beats the coin's mean by +4.68 bp (t 9.75, 83,303 cases), against -2.45 bp after the highest quintile (t -5.46).
