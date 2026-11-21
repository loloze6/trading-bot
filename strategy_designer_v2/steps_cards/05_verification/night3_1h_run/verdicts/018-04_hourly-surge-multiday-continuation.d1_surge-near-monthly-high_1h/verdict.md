---
plan: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move after long cases (return minus coin's normal 120-bar drift): 0.0037595; t of the mean: 1.58474 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: upper-half minus lower-half mean unusual move by entry forecast: 0.00356117, passed: True
- Counts: independent cases: 2364
- Decided by: The t-statistic lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Situation bars are those where the raw component (24h return in usual daily moves times proximity weight) is positive, on the long side; a case is the first long bet (forecast rise >= 2 points from its long trough) in each 120-bar grid cell from each window's first row, with a full 120-bar forward return inside the window; drift is the coin's mean non-overlapping 120-bar return over all windows; halves are the lower and upper n//2 cases by entry forecast (stable sort, middle case dropped if n is odd); fewer than 30 cases is reported as not observable.
- Size: unusual move +0.38 % per case over 120 bars, 0.036 of the coin's usual move (10.37 %); normal drift in its direction +0.65 %, total +1.02 %; 2364 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h`
Measure: `measure.py`
