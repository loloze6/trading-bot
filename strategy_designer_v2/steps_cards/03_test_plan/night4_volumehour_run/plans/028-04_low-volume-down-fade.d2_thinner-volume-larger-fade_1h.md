---
idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour with a fall far larger than the coin's typical hourly move over 30 days, on volume near or below its 30-day hourly average -> adapted: the on/off "far larger" and "near average" conditions become a graded product, the fall in usual moves times (k − volume ratio), read while it holds.
- Comparison: the hour's move against the 30-day typical hourly move, and its volume against the 30-day average hourly volume -> kept: both use 720-bar windows.
- Outcome: the price recovers part of the fall over the next two to six hours, more when the volume is thinner -> kept: a long held for 6 bars, sized up as the volume ratio falls.
- Verdict transfer: yes: the forecast is long in proportion to the fall times its thinness, so the 6-hour return after its bets tests the recovery claim in both directions.
Forecast: Two components share the same 720-bar return volatility s and the same hourly return r. The first, a, is the hour's return in usual moves, r/s. The second, b, is that return times the volume ratio v, where v is the hour's volume over its 720-bar mean. Each is standardised over 500 bars, negated and clipped at 0, so each is zero on up hours and grows with the depth of the fall. Each then goes through the strongest graded dead zone (signed_power, exponent 3, pivot 20), so ordinary hours stay near 0. The forecast is 2·a − b, which is proportional to fall × (constant − v). It is zero on up hours. It is positive after a fall on ordinary or thin volume and grows with the size of the fall and with how far the volume sits below its average. It turns negative only after falls on heavy volume, which the criterion leaves out. The cap of 20 limits the grading among the very deepest falls.
Config: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: The cases are the long bets: rises of the forecast on the long side of at least 2 points, read once per 6-bar grid cell of each window. For each case, take the coin's 6-bar return from the signal bar's close, minus the coin's normal 6-bar drift (holding the coin). The measure is the mean of these unusual moves over all cases, with its t, before costs.
- Supporting check: Split the long cases at their median volume ratio, v = last_history_value of fall_x_volume / last_history_value of fall. The mean unusual move of the thinner-volume half minus that of the heavier-volume half must be above 0.
- Confirm: The mean unusual move after long cases is positive with t ≥ 2, and the supporting check passes (thinner-volume half minus heavier-volume half > 0).
- Reject: The mean unusual move after long cases is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is t ≥ 2 when the thin-minus-heavy difference is ≤ 0. So is any result with fewer than 100 long cases pooled over both coins and all windows.
