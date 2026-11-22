---
idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour falling far more than its typical hourly move over the past 30 days, on volume several times its 30-day average -> adapted: the two thresholds become one graded product, the hour's fall in 720-bar return standard deviations times its volume over the 720-bar mean, damped by a cubic dead zone.
- Comparison: the fall against the typical hourly move, and the volume against the average hourly volume, both over 30 days -> kept: both use 720-bar windows.
- Outcome: the price rises over the next 3 to 24 hours, and more after larger falls -> adapted: "after the hour" becomes "while", and each bet is held 24 bars, the end of the stated span.
- Verdict transfer: yes: the forecast is long only on heavy-volume falls and grows with the fall, so the rebound's presence or absence after its cases decides the idea.
Forecast: The forecast uses one component, VolumeWeightedScaledReturnComponent (vol_period 720, volume_period 720). On each bar it computes the hour's return divided by the standard deviation of the last 720 hourly returns, times that hour's volume over its 720-bar mean. This value is standardised against its last 500 values (min_periods 120). It is then negated, so falls read positive. It is clipped at 0, so it is long only and zero on up hours. Last, signed_power with exponent 3 and pivot 10 damps ordinary moves to near zero. The forecast is therefore zero on rises and small on ordinary falls. It grows steeply as the fall gets larger against the hour's usual move and as the volume gets heavier against its average.
Config: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: A case is a bet: a rise of the forecast of at least 2 points, read once per 24-bar grid cell of each window. For each case, take the coin's 24-bar return from the signal bar's close, minus the coin's mean 24-bar return over all windows on non-overlapping stretches. The measure is the mean of these excess returns across both coins, with the t of that mean.
- Supporting check: Across the cases, the least-squares slope of the excess 24-bar return on the signal bar's forecast is positive. This tests that larger falls are followed by larger rebounds.
- Confirm: The mean excess return is positive with t ≥ 2, and the slope is above 0.
- Reject: The mean excess return is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with a slope at or below 0 is also inconclusive. So is a count below 30 cases over both coins.
