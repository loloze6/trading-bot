---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's short moving average of close is above its long one, the further its close sits below its short moving average, the more it falls over the following days.
Consequence: A trader would refuse or cut longs in an up-cross trend once price slips well beneath the short average, since that marks the trend's breakdown rather than a dip to buy.
Why:
- F2: The size of the spread is non-monotonic. Mean 10-bar excess by forecast bucket runs +0.004 (0–2), −0.017 (2–5), +0.012 (5–8), −0.008 (8–12) and +0.006 (12–20). By raw-spread octile it alternates sign, with t between −1.6 and +1.9.
- F6: Within the up-cross state, price sitting below its 50-day SMA is followed by losses. The lowest quartile of close/SMA50 averages −0.049 in 10-bar excess return (t −4.22, 124 blocks), against +0.020 in the third quartile (t 1.13).
