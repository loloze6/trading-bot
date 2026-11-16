---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return up to a moderate gain, the larger its rise over the next 10 days.
Consequence: A trader would size longs above the long average by how strong, but not yet stretched, the coin's 30-day run is, expecting the payoff within about 10 days.
Why:
- F4: The drift fades when the coin has already run far. Long bars whose past 30-day return is in the top fifth (above +44%) gain -0.000168 a day. The middle fifth (+15% to +28%) gains 0.004317. On the trending 10-bar grid, the 10-day forward return is +0.053 (t 2.95, n 126) for 30-day returns of +18% to +36%, but only +0.013 (t 0.67, n 126) for the top fifth.
