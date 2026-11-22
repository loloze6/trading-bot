---
idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: both thresholds are made graded as one product, the hour's return in 720-bar return standard deviations times its volume over the 720-bar mean volume, with a strong graded dead zone.
- Comparison: the typical hourly move and the average hourly volume over the past 30 days -> kept: a 720-bar return standard deviation and a 720-bar mean volume.
- Outcome: the price keeps rising over the next 24 hours, more as that hour's volume ratio is higher -> adapted: "after" becomes "while", each bet is held 24 bars, and size grows with the volume ratio.
- Verdict transfer: yes: the forecast is long exactly on high-volume sharp rises, sized by both, so the 24-bar moves after its bets confirm or reject the claim.
Forecast: The forecast uses VolumeWeightedScaledReturnComponent (vol_period 720, volume_period 720), computed at each hour's close. Its raw value is the hour's return divided by the standard deviation of the last 720 hourly returns, times the hour's volume over the mean of the last 720 hourly volumes. It is standardised over its past 500 values (min_periods 120) and clipped at 0, so only rises count and the forecast is long only, as the idea is. It then goes through signed_power with exponent 3 and pivot 20. An ordinary up hour reads about 10 after standardise and gives a forecast of about 2.5. A large rise on surging volume reaches the cap of 20 and gives a forecast of 20. Falls and flat hours give a forecast of 0. The size grows continuously with the move's size and with its volume ratio.
Config: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The unusual move of each case. A case is a bet: a rise of the forecast of at least 2 points, read once per non-overlapping 24-bar grid cell of each window. Its unusual move is the coin's 24-bar return from the signal bar's close minus the coin's normal 24-bar drift over all windows. Its strength is that unusual move divided by the coin's usual 24-bar move. The measure is the mean strength over all cases, with the t of that mean.
- Supporting check: The mean unusual move of cases whose forecast is above the cases' median, minus that of cases at or below it, is positive. This checks that a larger volume surge brings a larger further rise.
- Confirm: The mean unusual move is positive with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose supporting check fails, and so is a test with fewer than 30 cases in total (BTC and ETH together).
