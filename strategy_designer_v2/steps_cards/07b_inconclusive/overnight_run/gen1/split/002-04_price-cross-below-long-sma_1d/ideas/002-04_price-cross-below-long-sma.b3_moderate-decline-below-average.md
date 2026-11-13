---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is below its 200-day SMA after a moderate decline over the prior 30 days (around 10%, not a crash), the coin keeps falling over the next 10 days, by more than its usual drift.
Consequence: A trader would short coins that are drifting moderately below the average and stand aside after the sharpest 30-day drops, where rebounds follow.
Why:
- F9: Shorts taken after the steepest prior 30-day falls (bottom quartile, mean -27.5%) lose -0.009 (t = -0.89). Those after moderate falls (mean -10%) gain +0.014 (t = 1.90). Shorting after the sharpest drops runs into rebounds.
- F6: Deeper forecasts are not better and the response is not monotonic. The deepest forecast quintile (mean -16.7) loses -0.013 (t = -1.14), while the second quintile (mean -10.6) gains +0.013 (t = 1.53). The deepest raw-distance quintile (-45% below the SMA) gains -0.001 (t = -0.10). This matches the negative supporting slope of -0.0056.
