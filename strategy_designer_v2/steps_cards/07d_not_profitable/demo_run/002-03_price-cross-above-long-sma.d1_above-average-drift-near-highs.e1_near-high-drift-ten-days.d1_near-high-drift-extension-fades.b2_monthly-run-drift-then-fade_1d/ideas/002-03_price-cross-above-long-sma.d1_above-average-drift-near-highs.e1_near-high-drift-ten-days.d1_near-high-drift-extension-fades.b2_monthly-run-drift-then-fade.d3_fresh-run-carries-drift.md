---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average and its 30-day return is positive, the larger its 10-day return, the larger its rise over the next 10 days.
Consequence: A trader would add to a long in an uptrend when the latest ten days carry the run, and stay light when the month's gain is old.
Why:
- F6: Among trending cases with a positive 30-day return, the gain shows up mostly where the 10-day run is also strongest. The top 10-day-return quartile has a 10-day excess return of +0.049 (t 2.18, n 114), while the other quartiles lie between −0.001 and +0.014 (|t| ≤ 1.13).
- F1: The short side earns nothing and the long side carries the whole book. In the trending regime, short bars average a gain of 0.000174 per bar (t 0.53, n 2535, mean allocation −0.27), while long bars average 0.001244 (t 4.71, n 5918, mean allocation 0.41). Across all bars, shorts summed 0.43 against 7.38 for longs.
