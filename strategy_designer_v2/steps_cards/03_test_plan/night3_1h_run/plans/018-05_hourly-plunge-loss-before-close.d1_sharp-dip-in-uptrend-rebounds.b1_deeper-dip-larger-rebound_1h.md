---
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: a 24-hour fall of several times the 30-day average absolute daily return, read hourly, while the 30-day return is positive -> adapted: the "several times" threshold is made graded with a strong dead zone; "30-day return positive" is kept as a regime rule.
- Comparison: the coin's normal drift over the next 3 days -> kept.
- Outcome: the coin rises over the next 3 days, more so the deeper the fall -> kept, with a 72-bar horizon.
- Verdict transfer: yes: the forecast is long only in a 30-day rise and grows with the 24-hour fall in usual daily moves, so a confirm or reject of its 72-bar outcome transfers to the idea.
Forecast: The forecast is computed only while the coin's 720-bar (30-day) return is above 0. On other bars it is flat. - The measure is MeanAbsScaledReturnComponent with period 24 and window 720: the 24-hour return in multiples of the 30-day mean absolute 24-hour return. - Standardise puts it on the forecast scale (window 500, min_periods 120). Negate makes a fall read positive, and clip at min 0 keeps only falls, so the forecast is long only. - signed_power with exponent 3 and pivot 20 is the strongest graded dead zone. It keeps ordinary falls near 0, and the size grows steeply as the fall deepens toward several usual moves. - The forecast is 0 on rises and outside the 30-day uptrend.
Config: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The cases are bets: rises of the forecast of at least 2 points, read once per non-overlapping 72-bar grid cell of each window. For each case, take the coin's 72-bar return from the signal bar minus its normal drift (its mean 72-bar return over all windows), pooled across coins. Measure the mean of this unusual return with its t-statistic.
- Supporting check: Split the cases at their median forecast. The mean unusual 72-bar return of the larger-forecast half, minus that of the smaller-forecast half, must be above 0.
- Confirm: The mean unusual 72-bar return of the cases is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean unusual 72-bar return of the cases is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main measure that confirms while the larger-forecast half does not beat the smaller half is also inconclusive. At least 30 independent cases are required, else inconclusive.
