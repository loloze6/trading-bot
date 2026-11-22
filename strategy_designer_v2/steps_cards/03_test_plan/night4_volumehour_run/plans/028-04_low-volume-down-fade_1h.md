---
idea: 028-04_low-volume-down-fade
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour falling far more than its typical hourly move, on volume near its 30-day hourly average -> adapted: the "far more" threshold is made graded with the strongest graded dead zone, and volume near its average is kept as a regime condition.
- Comparison: the typical hourly move and the average hourly volume, each over the past 30 days (720 bars) -> kept
- Outcome: the price recovers part of the fall over the next two to six hours, more after a larger fall -> kept: long, held 6 bars.
- Verdict transfer: yes: the forecast is long only after quiet-volume falls, sized by the fall in usual moves, and held over the idea's horizon, so the test's result is the idea's result.
Forecast: The situation is read from one component, the last hour's return divided by the mean absolute hourly return over the past 720 bars (`MeanAbsScaledReturnComponent`, period 1, window 720). It is standardised over 500 bars, so one usual move is about 10. It is then negated so a fall reads positive, and clipped at 0 so it is long only. Finally `signed_power` with exponent 3 and pivot 20 damps ordinary falls: a fall of half a usual move gives about 0.3, one usual move gives 2.5, and two or more usual moves reach 20. The size therefore grows steeply with the depth of the fall. The forecast is active only in the `mean_reversion` regime. The detector selects it when that hour's volume is between 2/3 and 1.5 times its mean over the prior 720 bars (`VolumeRatioComponent`, period 720, exclude_current 1). On every other bar the regime is `unknown`, which is null, so the forecast is 0. It is never negative, and it is 0 on up hours and outside the volume condition.
Config: 028-04_low-volume-down-fade_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: Measured on the cases, which are the rises of the forecast of at least 2 points, read once per 6-bar grid cell of each window. For each case, the coin's 6-bar return from the signal bar's close minus its normal 6-bar drift (holding the coin, over all windows). The mean of this unusual move, and its t over the cases.
- Supporting check: Split the cases at their median forecast. The mean unusual move of the cases at or above the median must exceed that of the cases below it (the difference above 0).
- Confirm: The mean unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirm-level t whose supporting check fails. Fewer than 30 cases over both coins is also inconclusive.
