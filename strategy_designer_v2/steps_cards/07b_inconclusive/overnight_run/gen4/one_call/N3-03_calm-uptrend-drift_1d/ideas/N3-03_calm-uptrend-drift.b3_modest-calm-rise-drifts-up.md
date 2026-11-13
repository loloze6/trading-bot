---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.b inconclusive
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A calm coin whose 20-day return is modestly positive, in the lower-middle part of its usual positive range rather than at its largest, drifts up over the next five days.
Consequence: A trader would prefer calm, gently rising coins over calm coins that have just run up hard when choosing longs.
Why:
- F4: A larger forecast does not mean a larger drift. Forecast quartiles give +0.75%, +0.64%, +0.14% and +0.66% (all |t| < 1, about 224 cases each). By size of the 20-day return, only the second quartile stands out: +2.20%, t 2.45, n 191. The smallest quartile is −0.53% (t −0.88) and the largest +0.34% (t 0.37).
