---
plan: 031-03.b1.b1.b1_aligned-20-day-continuation_1d
idea: 031-03.b1.b1.b1_aligned-20-day-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x drift-removed 10-bar forward return: 0.0169284; day-clustered t of the mean: 1.85196 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: drift-removed directional return, |forecast| above minus below median (Welch difference): 0.00029624, passed: True
- Counts: grid cases: 2406, distinct days: 289
- Decided by: The main t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation check uses bars where both the 20-bar and 60-bar returns can be computed inside the window (the regime column only if none can); the coin's mean 10-bar return is the mean of all its non-overlapping grid returns over all windows; the day-clustered t sums deviations per UTC date; the supporting check splits cases strictly above/below the median |forecast| and passes when the high-minus-low mean difference is above 0.
- Size: unusual move +1.28 % (t 2.36, the cases of one day together: 1127 days) per case over 10 bars, 0.074 of the coin's usual move (16.82 %); normal drift in its direction -0.10 %, total +1.18 %; 2744 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.b1.b1.b1_aligned-20-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.b1.b1.b1_aligned-20-day-continuation_1d`
Measure: `measure.py`
