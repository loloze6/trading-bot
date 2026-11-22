---
idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: the two thresholds become one graded product, (hourly return / std of the last 720 hourly returns) x (volume / its 720-bar mean), cut to rises and damped to near zero away from the extreme.
- Comparison: the hour's rise against its typical 30-day hourly move, and its volume against its 30-day average -> kept: both are inside the component, over 720 bars.
- Outcome: the price keeps rising over the next 24 hours, more after heavier and larger hours -> kept: each bet is held for 24 bars and judged on the 24-bar return, with size following the product.
- Verdict transfer: yes: the test measures the same hour, the same two ratios and the same 24-hour rise, with only the thresholds made graded.
Forecast: The forecast uses one VolumeWeightedScaledReturnComponent with vol_period 720 and volume_period 720. It reads the last hour's return in units of the 30-day hourly standard deviation, times that hour's volume over its 30-day mean volume. This value is standardised over its past 500 values (min_periods 120) and clipped at 0, so a falling hour gives a forecast of 0. A signed_power with exponent 3 and pivot 20, the strongest dead zone allowed, then damps typical hours: a value of 10 becomes 2.5, 5 becomes 0.3, and 20 stays 20. The forecast is positive only after rising hours, and it grows steeply as both the scaled rise and the volume ratio grow. It is never negative.
Config: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The mean unusual 24-bar move after each case, with its t, pooled over both coins and all windows. A case is a bet: a rise of the forecast of at least 2, read once per 24-bar grid cell of each window. The unusual move is the coin's return from the case bar's close over the next 24 bars, minus the coin's normal 24-bar drift from holding it over all windows.
- Supporting check: Split the cases into halves by their forecast at the case bar. The mean unusual move of the top half minus that of the bottom half must be above 0.
- Confirm: The idea is confirmed when the mean unusual move has t ≥ 2 over at least 30 cases, and the supporting check passes (top half minus bottom half above 0).
- Reject: The idea is rejected when the mean unusual move has t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 with the top half not above the bottom half, and so is any result from fewer than 30 cases.
