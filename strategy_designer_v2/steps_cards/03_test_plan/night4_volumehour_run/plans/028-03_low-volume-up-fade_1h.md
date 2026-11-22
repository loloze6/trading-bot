---
idea: 028-03_low-volume-up-fade
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour rising far more than usual while volume stays near its 30-day hourly average -> adapted: "far more" made graded (hourly rise in usual moves, steep graded dead zone); volume near average kept as a regime gate (0.5 to 1.5 times the 720-bar mean).
- Comparison: the typical hourly move and the average hourly volume over the past 30 days -> kept: the 720-bar mean absolute hourly return and the 720-bar mean volume.
- Outcome: the price gives back part of the rise over the next two to six hours, more after larger rises -> kept: a short sized by the rise, held 6 bars.
- Verdict transfer: yes: the forecast is short only after quiet-volume up-hours, sized by the rise, and judged on the 6-hour giveback and its growth with size.
Forecast: The forecast uses one return measure, `MeanAbsScaledReturnComponent` (period 1, window 720). It is the last hour's return divided by the mean absolute hourly return of the past 720 hours. - It is standardised over 500 bars, with min_periods 120. - It is clipped at 0, so only up-hours count. - A cubic graded dead zone is applied (`signed_power` exponent 3, pivot 10), so ordinary rises give almost nothing and large ones dominate. - It is then negated. The forecast is never positive. It is negative after an up-hour, more negative the larger the rise in usual moves, and 0 after a down or flat hour. It is active only while the bar's volume is between 0.5 and 1.5 times its 720-bar mean. On all other bars it is 0, because those regimes are flat.
Config: 028-03_low-volume-up-fade_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: The cases are the short bets: the forecast falls by at least 2 points, read once per 6-bar grid cell. For each case, measure the 6-bar return from the signal bar's close minus the coin's normal 6-bar drift over all windows, signed short. Take the mean over cases, before costs.
- Supporting check: Split the cases at the median of the absolute forecast. The mean giveback of the larger half minus that of the smaller half must be above 0.
- Confirm: The main measure's mean giveback is above 0 with t >= 2, and the larger-half minus smaller-half difference is above 0.
- Reject: The mean giveback is below 0 with t <= -2, meaning the price continues upward after the quiet-volume rises.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t >= 2 with a check difference <= 0 is also inconclusive. Fewer than 100 independent cases across both coins is inconclusive.
