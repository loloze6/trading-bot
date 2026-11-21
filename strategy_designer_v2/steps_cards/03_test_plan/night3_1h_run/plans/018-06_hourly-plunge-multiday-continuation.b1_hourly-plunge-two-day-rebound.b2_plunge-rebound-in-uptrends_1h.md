---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5c26677afd57
---
Fidelity:
- Situation: the 24-hour return, read at an hourly close, falls by a large multiple of the 30-day average absolute daily return, while the 30-day return is positive -> adapted: the "large multiple" threshold is made graded, as the fall in usual daily moves times the positive 30-day rise, which is zero unless the 30-day return is positive.
- Comparison: the coin's usual 4-day drift -> kept
- Outcome: the price rises over the next 4 days, more as the 30-day rise is larger -> kept
- Verdict transfer: yes: the forecast is exactly the idea's fall-times-rise product, held for 4 days and judged against the coin's 4-day drift.
Forecast: The forecast uses one component, MeanAbsScaledFallTimesRiseComponent, at the idea's own settings: fall_period 24, window 720 (30 days) and rise_period 720 (30 days). Its value is the 24-hour fall in units of the 30-day mean absolute 24-hour return, times the positive 30-day percent return. It is zero after any 24-hour rise and whenever the 30-day return is not positive, and it grows with both the depth of the plunge and the size of the month's rise. It is standardised over its past 500 values (min_periods 120). A cubic graded dead zone (signed_power, exponent 3, pivot 10) then keeps small readings near zero and amplifies the rare extremes. The forecast is never negative, so the strategy is long only.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h_config.json
Criterion:
- Horizon: 96 bars
- Main measure: Over the cases (forecast rises of at least 2 points, one per 96-bar grid cell of each window), take the coin's 96-bar return from the signal bar's close minus its normal 96-bar drift (the mean over non-overlapping 96-bar stretches of all its windows). The measure is the mean of this unusual move over all coins and windows, with its t of the mean, before costs.
- Supporting check: Split the cases at the median forecast at entry. The mean unusual move of the cases above the median minus that of the cases below it must be above 0.
- Confirm: Mean unusual move above 0 with t >= 2 on at least 30 cases, and the supporting check above 0.
- Reject: Mean unusual move below 0 with t <= -2 on at least 30 cases.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check not above 0, or fewer than 30 cases. The minimum is 30 cases across all coins and windows.
