---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-06_deep-below-average-rebound
line: 7.b inconclusive
backtest: N1-06_deep-below-average-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close is far below its 200-day average and the coin has also just fallen sharply over the last two weeks, its price rises over the next ten days more than its usual drift.
Consequence: A trader should take the below-average rebound long only right after a sharp recent fall, and refuse it when the coin is merely sitting deep below the average.
Why:
- F1: Across the 201 non-overlapping deep cases (forecast ≥ 5), the mean excess 10-bar return is only +0.0099 with a hit rate of 52% and t = 0.88. These cases fall on just 97 distinct dates, and once they are clustered by date the t drops to 0.23, so the pooled effect is small and largely one shared market move counted several times.
- F3: Depth below the SMA200 does not drive the rebound. Within the deep cases the deepest raw-distance tercile earns +0.001 (hit 45%, n = 67), against +0.012 for the shallowest (hit 60%). The forecast bucket 5–10 is also negative at −0.005 (n = 99), even though the overall slope is positive.
- F4: The rebound sits in deep cases that also fell sharply over the prior 10 bars. Deep cases that fell 15% or more earn +0.049 excess (hit 59%, t = 1.96, n = 56, 29 dates, date-clustered t = 1.11). The other 145 deep cases earn −0.005 (t = −0.44). The tercile that fell most earns +0.045 (t = 1.89, n = 61).
- F7: The crash rebound is not specific to one coin. Deep crash cases are positive in 5 of 6 coins: LTC +0.054 (n = 11), XRP +0.157 (n = 7), ZEC +0.028 (n = 14), ETH +0.039, XMR +0.040. BTC is the exception at −0.008 (n = 6).
