---
idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour that rises far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: the two thresholds are made graded as one product, the hour's rise in 720-bar return standard deviations times its volume over the 720-bar mean volume, long side only, with a cubic graded dead zone.
- Comparison: the typical hourly move and the average hourly volume over the past 30 days -> kept: a 720-bar return standard deviation and a 720-bar mean volume.
- Outcome: the price keeps rising over the next six hours, more after larger relative rises -> adapted: "after" becomes "while" (the bet is opened on the surge bar's close) and is held 6 bars.
- Verdict transfer: yes: the forecast is large only when a strong rise and heavy volume occur together, it grows with both, and the 6-hour rise that follows is what is measured.
Forecast: The forecast uses one component, the volume-weighted scaled return with vol_period 720 and volume_period 720. It is the current hour's return divided by the standard deviation of the last 720 hourly returns, times the hour's volume over its 720-bar mean. - It is standardised against its own last 500 values (min_periods 120), then clipped at 0, so only rises count. - It is then cubed with signed_power (exponent 3, pivot 10). The result is near zero on ordinary hours and grows steeply as the rise and the volume ratio grow together. - It is positive (long) after a heavy-volume up-hour and 0 otherwise. It is never short.
Config: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: For each case, take the coin's 6-bar return from the signal bar's close minus the coin's normal 6-bar drift (the unusual move). A case is a forecast rise of at least 2 points, read once per 6-bar grid cell of each window. The measure is the ordinary t of the mean over BTC and ETH pooled.
- Supporting check: Split the cases at the median entry forecast. The mean unusual move of the top half minus that of the bottom half must be above 0, so the follow-through grows with the surge.
- Confirm: The mean unusual move is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t >= 2 with the supporting check failing, or fewer than 30 cases in total.
