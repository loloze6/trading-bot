---
idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the 5-day average volume against the 30-day average, higher or lower -> kept
- Comparison: higher ratio against lower ratio, whatever the direction of the last 5 days -> kept: the forecast reads only volume and never the price direction
- Outcome: a higher return over the next 7 days as the ratio rises -> kept: horizon of 7 bars
- Verdict transfer: yes: the forecast is the idea's own graded ratio, and the measure is the idea's own 7-day return relation.
Forecast: The forecast uses one indicator, the log of the mean volume over the last 5 bars divided by the mean volume over the last 30 bars (bar t included in both). It is standardised against its own past 60 values, with a minimum of 20. It is positive, so long, when recent volume runs above the 30-day norm. It is negative, so short, when volume has dried up. It is near 0 at the norm. Its size grows continuously with the log ratio and is capped at ±20. Price direction is not used.
Config: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The slope t of a pooled OLS regression across all coins and windows. The dependent variable is the coin's 7-bar forward return close[t+7]/close[t]-1 minus that coin's mean 7-bar return over all windows. The regressor is the forecast at bar t. The sample uses non-overlapping bars at positions 0, 7, 14, … of each window.
- Supporting check: On the same samples, the mean excess 7-bar return of the top forecast tercile minus that of the bottom tercile must be above 0.
- Confirm: The slope has t ≥ 2 and the top-minus-bottom tercile difference is above 0.
- Reject: The slope has t ≤ -2.
- Inconclusive: The slope t lies between -2 and 2, or t ≥ 2 but the tercile difference is 0 or below. At least 300 independent non-overlapping cases are needed; about 2,400 are expected.
