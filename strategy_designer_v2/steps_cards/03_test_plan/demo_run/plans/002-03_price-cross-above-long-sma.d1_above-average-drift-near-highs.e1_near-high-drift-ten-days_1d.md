---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: close above its 200-day average, and where the close sits in its 20-day close range -> kept: a regime rule on the close's distance to SMA200 and the 20-close range position.
- Comparison: higher in the 20-day range against lower in it -> kept: the forecast is graded by range position.
- Outcome: a larger rise over the next 10 days -> kept: the 10-bar forward return is measured.
- Verdict transfer: yes: the test measures the stated condition, the stated graded relation and the stated 10-day rise directly.
Forecast: The forecast is active only while the close is at or above its 200-day simple average. That is the regime `trending`; every other bar is flat. While it is active, the forecast is the close's position in the range of its last 20 closes, current bar included. It runs from -20 at the range low, through 0 at mid-range, to +20 at the range high. It is standardised against its own past 60 values, so an average reading is about 10, capped at ±20. The forecast is positive when the close is in the upper half of the range and negative in the lower half, and it grows continuously as the close nears the 20-day high.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use bars in regime `trending`, on the non-overlapping 10-bar grid of each window. Regress the coin's 10-bar forward return minus that coin's mean 10-bar return over all windows on the bar's forecast, pooled over coins and windows. The measure is the slope's t-statistic.
- Supporting check: On the same cases, the mean excess 10-bar return of the top third of forecasts minus the bottom third must be above 0.
- Confirm: The idea is confirmed when the slope is positive with t ≥ 2 and the top-minus-bottom-third difference is above 0.
- Reject: The idea is rejected when the slope is negative with t ≤ -2.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. A t ≥ 2 with a top-minus-bottom difference at or below 0 is also inconclusive. The test needs at least 100 independent grid cases in regime `trending`; fewer is inconclusive.
