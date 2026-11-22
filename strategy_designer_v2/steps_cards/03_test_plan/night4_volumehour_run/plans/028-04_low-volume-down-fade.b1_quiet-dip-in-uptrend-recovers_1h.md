---
idea: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour falling far more than the 30-day typical hourly move, on volume near its 30-day average, in a positive 7-day return -> adapted: the fall size is graded (in mean absolute 1h moves over 720 bars) and multiplied by the positive 168-bar return; volume near average is a regime condition.
- Comparison: the fall against the typical 30-day hourly move, the volume against its 30-day average, refused in a 7-day decline -> kept: the component reads 0 when the 168-bar return is not positive.
- Outcome: the price recovers part of the fall over the next six hours, more so the larger the 7-day rise (long) -> kept: 6-bar hold, size growing with fall times rise.
- Verdict transfer: yes: the forecast is the idea's quiet-volume drop scaled by the 7-day rise, held six hours, so its result is the idea's result.
Forecast: The forecast is long only, and only while the current bar's volume is between 0.67 and 1.5 times its 720-bar mean (the regime). It is the component MeanAbsScaledFallTimesRiseComponent (fall_period 1, window 720, rise_period 168). The component multiplies the size of the current hour's fall, counted in mean absolute 1h moves over 720 bars, by the positive 168-bar percent return. It is standardised over 500 bars, then signed_power with exponent 3 and pivot 20 is applied: the strongest graded dead zone, so ordinary dips stay near 0 and only large falls in strong 7-day rises reach large positions. It is 0 on up hours, in 7-day declines, and outside the volume band. It is never negative.
Config: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: A case is a long bet (a forecast rise of at least 2), read once per 6-bar grid cell of each window. The measure is the mean unusual move over the cases: the coin's 6-bar return from the signal bar's close minus the coin's mean 6-bar return over all windows. Its t is the t of the mean, counted over the cases of BTC and ETH together.
- Supporting check: Across the cases, the correlation between the signal bar's forecast and the unusual move is above 0 (larger dip in a stronger rise, larger recovery).
- Confirm: The mean unusual move is above 0 with t >= 2 and the supporting check passes.
- Reject: The mean unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is t >= 2 when the check fails. Fewer than 30 cases is inconclusive whatever the t.
