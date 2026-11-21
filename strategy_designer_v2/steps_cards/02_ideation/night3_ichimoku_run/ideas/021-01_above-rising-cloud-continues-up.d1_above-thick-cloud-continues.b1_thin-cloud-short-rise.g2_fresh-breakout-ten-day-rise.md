---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its Ichimoku cloud (9/26/52), its return over the next 10 days is larger the fewer days have passed since its close first rose above the cloud.
Consequence: A trader could hold a fresh breakout above the cloud for about two weeks rather than one, since the extra rise keeps building past five days.
Why:
- F1: Among bars where a coin closes above its Ichimoku cloud, the fewer days since it crossed above, the larger its next 5-day return above its normal drift. The slope on the log of days since crossing is -0.0215 (t -3.65, 490 non-overlapping cases), and the pattern holds in both halves of the windows (w1-w12: t -3.11, n 282; w13-w24: t -2.07, n 208).
- F4: The freshness effect lasts beyond the tested horizon: over the next 10 days the slope on log days since crossing is -0.0350 (t -3.66, 432 cases on the 5-day grid, so the cases overlap).
- F5: The coins mostly agree on freshness: 5 of 6 coins have a negative slope (XRP t -2.86, LTC -1.70, ETH -1.63, ZEC -1.38, XMR -1.04), and BTC alone is flat (+0.0026, t 0.32, n 87).
