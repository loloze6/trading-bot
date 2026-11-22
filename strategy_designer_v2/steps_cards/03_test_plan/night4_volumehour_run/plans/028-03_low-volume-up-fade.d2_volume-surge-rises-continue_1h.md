---
idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: the threshold becomes graded, as the hour's return in 30-day standard deviations times its volume over the 30-day mean, with long side only and a cubic dead zone; "after" becomes "while".
- Comparison: the higher the hour's volume against its 30-day average, the larger the further rise; ordinary volume gives no edge -> kept: the volume ratio multiplies the position, and ordinary-volume rises sit in the dead zone near zero.
- Outcome: the price keeps rising over the next six hours -> kept: each bet is held 6 bars.
- Verdict transfer: yes: the forecast is the idea's surge rise graded by the idea's own two ratios and held for its six hours.
Forecast: One component, VolumeWeightedScaledReturnComponent, with vol_period 720 and volume_period 720 (30 days of 1h bars). It computes the last hour's return divided by the standard deviation of hourly returns over 30 days, times that hour's volume over its 30-day mean. It is standardised over its past 500 values (min_periods 120) and clipped at 0, so only rises go long. A cubic dead zone (signed_power, exponent 3, pivot 20) then keeps ordinary hours near zero: a standardised 10 becomes 2.5, 5 becomes 0.3 and 20 stays 20. The forecast is positive and large only on an hour with a big rise on a volume surge. It grows with both the size of the move and the volume multiple. It is zero on falling hours and never negative.
Config: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: A case is a long signal: a rise of the forecast of at least 2 points, read once per 6-bar grid cell of each window. For each case, take the coin's 6-bar return from the signal bar's close, minus the coin's normal 6-bar drift (holding the coin, over all windows). Pool the cases over BTC and ETH and all windows, and take the t of the mean of this unusual move.
- Supporting check: Split the cases at the median forecast on the signal bar. The mean unusual move of the upper half minus that of the lower half must be above 0, since the idea says stronger surges carry further.
- Confirm: The mean unusual 6-bar move is positive with t ≥ 2, and the supporting check is above 0.
- Reject: The mean unusual 6-bar move is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 with the supporting check at or below 0. So is any result from fewer than 30 cases in total.
