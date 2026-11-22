---
idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume above its 30-day average -> adapted: "far more" made graded by a convex dead zone on the rise in typical moves; the volume condition is kept as a regime rule.
- Comparison: the hour's rise against the 30-day mean absolute hourly move, and its volume against the 30-day mean hourly volume -> kept
- Outcome: price keeps rising over the next 24 hours, more after larger rises in typical moves -> kept
- Verdict transfer: yes: the forecast is long only on above-average-volume hours, grows with the rise in typical moves and is held 24 bars, so its result is the idea's.
Forecast: The forecast is computed only on hours whose volume is at or above the mean volume of the prior 720 hours (VolumeRatioComponent, period 720, bar excluded from the base, ratio at least 1.0). On every other hour the regime is null and the forecast is 0. On qualifying hours the forecast is the hour's return divided by the mean absolute hourly return of the last 720 hours (MeanAbsScaledReturnComponent, period 1, window 720). That value is then reshaped in three steps: - standardise (window 500, min_periods 120) puts it on the forecast scale; - signed_power (exponent 3, pivot 20) applies the strongest graded dead zone the guide allows, so an ordinary hour gives almost nothing (standardised 10 gives 2.5) while a large rise grows convexly up to 20; - clip at a minimum of 0 makes it long only, so falling hours give 0. The forecast is positive only after a rising, above-average-volume hour, and it grows with the size of that rise in typical moves. Each bet is held 24 bars.
Config: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are rises of the forecast of at least 2 points, read once per cell of a 24-bar grid in each window. For each case, take the coin's 24-bar return from the signal bar's close minus the coin's mean 24-bar return over all windows. The measure is the mean of these excess returns over all cases, with its t.
- Supporting check: The mean excess return of cases whose forecast is above the cases' median, minus that of cases at or below it, must be greater than 0.
- Confirm: The mean excess return is positive with t ≥ 2 over at least 30 cases, and the supporting check is positive.
- Reject: The mean excess return is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a supporting check that is not positive is also inconclusive. Fewer than 30 cases is inconclusive whatever the t.
