---
idea: 028-01_volume-surge-up-continuation
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume several times its 30-day hourly average -> adapted: the two thresholds become one graded product, (hour's return / 720-bar std of hourly returns) x (hour's volume / 720-bar mean volume), with a strong graded dead zone.
- Comparison: the larger that hour's volume against its usual volume, the larger the further rise -> kept: the forecast grows with the volume ratio, and the check measures the rise against it.
- Outcome: the price keeps rising over the next two to six hours -> kept: each bet is held 6 bars, the end of the idea's range.
- Verdict transfer: yes: the forecast is largest after large up-hours on heavy volume, so its bets measure this rise and its link to volume directly.
Forecast: The forecast uses one component, VolumeWeightedScaledReturnComponent with vol_period 720 and volume_period 720, which are 30 days of hourly bars. Its value is the hour's return in usual hourly moves times the hour's volume against its 30-day mean. It is standardised over its past 500 values (min_periods 120), so an ordinary hour reads about 10. It then passes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone: an ordinary hour gives about 2.5 or less, and an extreme hour gives up to 20. Last, a clip at min 0 makes it long only, because the idea claims only rises after up-hours. The forecast is positive after up-hours and grows steeply as the move and the volume surge both get larger. It is 0 after down-hours and near 0 on ordinary hours. It is never negative.
Config: 028-01_volume-surge-up-continuation_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: Cases are the long bets: a rise of the forecast of at least 2 points, read once per 6-bar grid cell of each window. For each case, take the coin's 6-bar return from the signal bar's close, minus the coin's mean 6-bar return over all windows (holding the coin). The measure is the mean of this excess return over the cases, before costs, with its t.
- Supporting check: Among cases at or after bar 720 of their window, recompute the volume ratio from the recorded bars: volume over the mean of the prior 720 bars' volume. Regress the cases' excess 6-bar return on this ratio. The slope must be above 0.
- Confirm: The idea is confirmed when the mean excess 6-bar return over the cases has t ≥ 2, with at least 100 cases, and the supporting slope is above 0.
- Reject: The idea is rejected when the mean excess return has t ≤ -2 with at least 100 cases, or when the slope of excess return on volume ratio has t ≤ -2.
- Inconclusive: Any main t between -2 and 2 is inconclusive. So is a confirming main measure with a slope at or below 0 whose t is above -2. Fewer than 100 cases is also inconclusive, whatever the t.
