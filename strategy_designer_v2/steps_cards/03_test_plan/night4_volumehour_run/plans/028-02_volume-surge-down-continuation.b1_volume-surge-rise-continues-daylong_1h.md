---
idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume several times its 30-day hourly average, larger with rise times relative volume -> adapted: the thresholds "far more" and "several times" become graded, as the product (hour's return / 720-bar return std) x (volume / 720-bar mean volume), long side only, with a strong graded dead zone.
- Comparison: the rise against the typical hourly move, and the volume against the average hourly volume, both over the past 30 days -> kept: both are ratios over 720 bars.
- Outcome: price keeps rising over the next 24 hours, more for a larger product -> kept: each bet is held 24 bars and judged on the 24-bar return.
- Verdict transfer: yes: the forecast is the idea's own product on the idea's own windows and horizon, so a confirm or a reject on it is a confirm or a reject of the idea.
Forecast: The forecast uses VolumeWeightedScaledReturnComponent with vol_period 720 and volume_period 720. Its raw value is the hour's return divided by the 720-hour standard deviation of hourly returns, times the hour's volume over its 720-hour mean. The value is standardised against its past 500 values (min_periods 120). Clipping at 0 makes it long only, so it never shorts: falls and quiet hours give 0. signed_power with exponent 3 and pivot 10 then damps ordinary hours to near 0 and amplifies the rare large rises on heavy volume. The forecast is positive only after an up hour and grows continuously with the rise times its relative volume. Each rise of the forecast is held for 24 bars.
Config: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The mean unusual move over the cases. A case is a bet: a rise of the forecast of at least 2 points, read once per 24-bar grid cell in each window. Its unusual move is the coin's return from the case's close over the next 24 bars, minus the coin's normal 24-bar drift over all windows. The t of this mean is reported with the count of cases.
- Supporting check: Split the cases at the median forecast. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The main measure has a mean above 0 with t ≥ 2, and the supporting check passes.
- Reject: The main measure has a mean below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or a confirming t with a failed supporting check, is inconclusive. Fewer than 30 cases across both coins and all windows is also inconclusive.
