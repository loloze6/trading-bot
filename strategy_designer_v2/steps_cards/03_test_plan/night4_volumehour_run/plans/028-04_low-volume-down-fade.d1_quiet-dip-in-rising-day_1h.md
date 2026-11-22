---
idea: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour falling far more than its 30-day typical hourly move, on volume near its 30-day average, after a 24-hour rise -> adapted: the fall in 30-day mean absolute hourly moves times the prior 24h rise (graded, with a dead zone for "far"); "volume near average" kept as a regime condition.
- Comparison: typical hourly move and average hourly volume over the past 30 days; the 24h return before that hour -> kept.
- Outcome: price recovers part of the fall over the next 2 to 6 hours, more after a larger prior rise (long) -> kept: a long held 6 bars, sized by the rise.
- Verdict transfer: yes: the graded product and the volume band measure the idea's own quantities, so a confirm or reject carries over.
Forecast: The regime is `mean_reversion` only while the hour's volume is between 0.67 and 1.5 times its mean over the prior 720 hours. On every other bar the forecast is 0. Inside that regime, the forecast comes from one component. It is the hour's fall, counted in 720-hour mean absolute hourly moves, times the percent rise of the 24 hours before that hour. - It is 0 when the hour did not fall or when the prior 24h did not rise. - It is standardised over 500 bars. - It then goes through `signed_power` with exponent 3, so ordinary dips stay near 0 and only large falls inside strong rises give a sizeable long. - It is never negative.
Config: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: Take each case (a long bet: a forecast rise of at least 2 points), one per 6-bar grid cell of each window. Measure the coin's 6-bar return from the signal bar's close minus the coin's mean 6-bar return over all windows (the unusual move). Pool the cases over coins and windows and compute the t of their mean.
- Supporting check: Across the cases, the mean unusual move weighted by the forecast at the signal must be above 0.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the forecast-weighted mean is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a confirming t whose weighted mean is not above 0, or fewer than 30 independent cases.
