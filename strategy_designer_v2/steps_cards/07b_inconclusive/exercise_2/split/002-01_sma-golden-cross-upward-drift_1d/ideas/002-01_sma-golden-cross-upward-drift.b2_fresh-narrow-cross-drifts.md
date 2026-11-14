---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 50-day SMA has only recently moved above its 200-day SMA and the spread is still small, the coin's next 10 bars rise more than its typical 10-bar move.
Consequence: A trader would concentrate long exposure on young, narrow golden crosses and not on mature, wide ones.
Why:
- F5: There is no monotonic grading by forecast size:
- F8: By raw 50/200 spread among up-spread blocks, the two smallest quintiles earn +0.0054 and +0.0085 excess and the largest quintile -0.0073, all with |t| < 0.71. The share of positive returns while active is 2.1 points below each coin's base rate (-0.0214).
- F3: Demeaned within each window instead of per coin, the slope turns clearly negative at -0.00163 (t -3.08). Most window slopes are negative, for example w16 at -0.0220 (t -5.73), w18 at -0.0106 (t -3.22) and w1 at -0.0163 (t -2.66), and the 2020 and 2022 slopes are also negative (t -2.22 and -2.42). The flat pooled slope therefore comes from active periods coinciding with strong market periods, not from the forecast ranking returns within a period.
