---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.b inconclusive
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is in the lower half of its last 100 days and its 20-day return is zero or negative, its price drifts down over the next five days.
Consequence: A trader would refuse longs, or lean short, in a coin that is falling quietly, rather than treat calm as a sign of safety.
Why:
- F3: The calm-and-falling side is the clearer half. Bars in the calm regime with a 20-day return at or below zero (forecast 0) are followed by a mean 5-bar excess return of −0.66% (t −2.12, n 912). Calm rising bars give +0.55% and all bars give +0.02% (t 0.11, n 3419), so the calm long-minus-flat spread is about 1.2% per 5 bars.
- F1: The effect is small and spread thin. On long bars, the mean 5-bar excess return is +0.55% with t = 1.49 over 897 non-overlapping cases. No single coin reaches t = 1.3: LTC is +1.16% (t 1.29, n 159), XRP +1.52% (t 1.05, n 122), BTC +0.01% (t 0.01, n 169) and XMR −0.16% (t −0.25, n 168). Long bars are as noisy as all bars (std of 5-bar return 11.0% against 11.1%).
