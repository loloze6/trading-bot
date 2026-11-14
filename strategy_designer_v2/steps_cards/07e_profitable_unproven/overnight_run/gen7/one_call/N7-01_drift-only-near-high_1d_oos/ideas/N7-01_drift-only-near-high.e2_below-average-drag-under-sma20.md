---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.e profitable but not proven
backtest: N7-01_drift-only-near-high_1d_oos
instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
bar: 1d
period: folds A, D
---
Idea: In one coin, the day after a close below its 20-day simple average, the return is below the coin's average.
Consequence: Refuse or exit longs in a coin while its close is under its 20-day average, since that state carries below-average next-day returns.
Why:
- F7: Being above SMA20 without a recent 20-day high earns nothing. Those coin-days have next-day excess −0.0016 (t = −1.02, n = 1005). By contrast, all coin-days below SMA20 have −0.0014 (t = −2.25, n = 5780), and all coin-days above it have +0.0010 (t = 1.31, n = 5009).
- F3: The gain is earned in a few strong-market windows, not spread evenly. In-market coin excess over the coin's all-window mean is +0.0083 in w6 (t = 4.66, n = 699 coin-days) and +0.0089 in w9 (t = 3.06, n = 593), when the market averaged +0.0086 and +0.0073 a day. It is −0.0118 in w10 (t = −2.92, n = 146), −0.0081 in w3 (t = −2.32, n = 276) and −0.0074 in w12 (t = −2.22, n = 139).
