---
idea: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour falling far more than its 30-day typical hourly move, on volume several times its 30-day average -> adapted: the two thresholds become one graded product (fall in 30-day standard deviations × volume over its 30-day mean), with a cubic dead zone.
- Comparison: the fall against the 30-day typical hourly move, and the volume against the 30-day average hourly volume -> kept: both use 720-bar windows.
- Outcome: the price recovers part of the fall over the next two hours, more so on higher volume -> kept: long, held 2 bars.
- Verdict transfer: yes: the product is large only when the fall is large in usual moves and grows with the volume ratio, so a confirm or reject on what follows the largest positions carries over to the idea.
Forecast: The forecast uses one indicator, VolumeWeightedScaledReturnComponent (vol_period 720, volume_period 720). Its raw value is the hour's return divided by the 30-day standard deviation of hourly returns, times the hour's volume divided by its 30-day mean. It is standardised over its last 500 values, then negated so a heavy-volume fall reads positive. It is clipped at 0, so it is long only and zero on any rising hour. Last, it is cubed with signed_power (exponent 3, pivot 10). This keeps ordinary falls near zero and makes the position grow steeply with a deeper fall and a larger volume surge. The forecast is positive only after a falling hour, largest after an extreme fall on extreme volume, and never negative.
Config: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Cases are bets (the forecast rising by 2 points or more), read once per non-overlapping 2-bar grid cell in each window, for both coins and all windows pooled. For each case, take the coin's 2-bar return from the signal bar's close minus the coin's normal 2-bar drift over all windows. The measure is the mean of this unusual move and its t, before costs.
- Supporting check: Recompute each case's volume ratio from the bars (volume over its 720-bar mean). Split the cases at the median volume ratio. The mean unusual move of the top half minus that of the bottom half must be above 0.
- Confirm: Confirmed when the mean unusual move is above 0 with t ≥ 2 on at least 30 cases, and the supporting check passes.
- Reject: Rejected when the mean unusual move is below 0 with t ≤ -2 on at least 30 cases.
- Inconclusive: Inconclusive when t is between -2 and 2, or when t ≥ 2 but the volume split is not positive, or when there are fewer than 30 cases.
