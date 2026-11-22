---
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour falling far more than its typical hourly move over 30 days, on volume several times its 30-day hourly average -> adapted: both thresholds made graded as one product, (fall in 720-bar standard deviations) x (volume / 720-bar mean volume), with a strong graded dead zone; "after the hour" becomes "at that hour's close".
- Comparison: the typical hourly move and the average hourly volume over the past 30 days -> kept: a 720-bar return standard deviation and a 720-bar mean volume.
- Outcome: the price rebounds (rises) over the next two hours, more after a larger fall -> kept: long, held 2 bars, sized by the fall.
- Verdict transfer: yes: the forecast is long only on heavy-volume falls, grows with their size, and is held for the idea's two hours.
Forecast: The forecast uses VolumeWeightedScaledReturnComponent with vol_period 720 and volume_period 720. Its raw value is the hour's return divided by the 30-day standard deviation of hourly returns, times the hour's volume over its 30-day mean volume. This value is standardised over 500 bars (min_periods 120), then negated so that a fall reads positive. It is clipped at 0, so up hours give a forecast of 0 and the book is long only. Then signed_power with exponent 3 and pivot 10 is applied: ordinary falls stay near 0, and only large falls on heavy volume give a sizeable long. The long grows steeply with both the depth of the fall and the volume ratio, and is capped at +20. The forecast is never negative.
Config: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are bets: a rise of the forecast of at least 2 points, read once per cell of a 2-bar grid in each window. For each case, take the coin's 2-bar return from the signal bar's close, minus the coin's normal 2-bar drift (its mean over all windows). Measure the mean of these unusual moves over all cases, and its t, before costs.
- Supporting check: Among the cases, the slope of the unusual move on the forecast at the signal bar is positive. A larger forecast means a larger fall, so this tests whether the rebound grows with the fall.
- Confirm: The mean unusual move is positive with t >= 2, and the supporting slope is positive.
- Reject: The mean unusual move is negative with t <= -2, meaning the heavy-volume falls extend rather than rebound.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a positive t >= 2 with a slope that is zero or negative. At least 30 independent cases across both coins are needed, or the result is inconclusive.
