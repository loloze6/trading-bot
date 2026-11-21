---
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return -> adapted: the "several times" threshold becomes graded, the fall in usual daily moves with a strong graded dead zone.
- Comparison: the 30-day return is positive, and larger in multiples of its usual 30-day move -> kept: the positive 30-day rise multiplies the fall and is zero otherwise; standardise rescales it against the coin's own past, so the rise is read relative to the coin's usual size.
- Outcome: the coin rises over the next 3 days more than its normal drift, and more for a larger 30-day rise -> kept: long held for 72 bars, judged against the coin's normal 72-bar drift.
- Verdict transfer: yes: the forecast is non-zero only on a sharp daily fall inside a monthly rise, and it grows with both, as the idea states.
Forecast: One component, MeanAbsScaledFallTimesRiseComponent with fall_period 24, window 720 and rise_period 720. Its raw value is the 24-hour fall in multiples of the 30-day mean absolute 24-hour return, times the positive 30-day percent return. It is 0 when the last 24 hours did not fall or when the 30-day return is not positive, so the forecast is never negative (long or flat). Standardise rescales it against its own last 500 values (min_periods 120). Signed_power with exponent 3 and pivot 20, the strongest graded dead zone allowed, then keeps small falls and weak monthly rises near 0. The forecast grows smoothly with a deeper fall and a stronger month's rise, and the combined forecast is capped at +20.
Config: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Cases are bets: rises of the forecast of at least 2 points, read once per 72-bar grid cell of each window. For each case, take the coin's 72-bar return from the signal bar's close minus the coin's normal 72-bar drift (its mean over all windows). The measure is the mean of these unusual moves, with the t of that mean.
- Supporting check: Among the cases, the unusual move must grow with the forecast at entry, so that cases above the median entry forecast have a larger mean unusual move than those below it (Welch difference, upper minus lower, greater than 0).
- Confirm: Mean unusual move above 0 with t >= 2 over at least 30 independent cases, and the supporting check's difference above 0.
- Reject: Mean unusual move below 0 with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, fewer than 30 independent cases pooled over coins and windows, or a confirming mean whose supporting check fails.
