---
idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour in which the coin falls far more than its typical hourly move -> adapted: "far more" becomes graded, with a strong graded dead zone instead of a threshold.
- Comparison: typical hourly move over the past 30 days -> kept: the hour's return is divided by the mean absolute hourly return over 720 bars.
- Outcome: price recovers part of the fall over the next three hours, more after deeper falls -> kept: long, held 3 bars, size growing with the fall's depth.
- Verdict transfer: yes: the forecast is long only after an hour's fall, sized by its depth in 30-day typical hourly moves, and held for three hours, so a rebound or its absence in the record speaks for the idea itself.
Forecast: The forecast starts from the hour's return divided by the coin's mean absolute hourly return over the past 720 bars (30 days). This is MeanAbsScaledReturnComponent with period 1 and window 720. It is standardised over its past 500 values (min_periods 120), so a fall of one typical move reads about -10. It is then negated, so a fall reads positive, and clipped at 0, so up hours give 0. Last, it is raised with signed_power at exponent 3 and pivot 10, the strongest graded dead zone. Small falls are damped close to 0: a fall of half a typical move gives about 1.25. Falls of one typical move or more grow quickly toward the cap of +20. The forecast is never negative. It is 0 on up or flat hours and positive after a falling hour, growing with the depth of the fall.
Config: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are bets: rises of the forecast of at least 2 points, read once per 3-bar grid cell in each window. For each case, take the coin's return from the close of the signal bar over the next 3 bars, minus the coin's normal 3-bar drift from holding it. Measure the mean of this unusual move over the cases of both coins, and its t.
- Supporting check: Split the cases into terciles by forecast size at the signal bar. The top tercile's mean unusual move minus the bottom tercile's must be greater than 0. This tests that deeper falls bring larger recoveries.
- Confirm: The mean unusual move is positive with t ≥ 2, and the supporting check passes (top tercile minus bottom tercile greater than 0).
- Reject: The mean unusual move is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 when the top tercile does not beat the bottom one. The test needs at least 100 non-overlapping cases across both coins; with fewer, the result is inconclusive.
