---
plan: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move of long cases (return minus coin's normal 120-bar drift): 0.00350547; t of the mean: 1.84596 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: upper-half minus lower-half mean unusual move (by signal forecast): 0.00496779, passed: True
- Counts: cases: 4984, upper_half_cases: 2492, lower_half_cases: 2492
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet) in each 120-bar grid cell counted from each window's first row, kept only if its 120-bar return lies inside the window; the halves are the forecast-sorted lower and upper n//2 cases (middle case dropped when n is odd); the situation is a positive raw component value (upside surge).
- Size: unusual move +0.35 % per case over 120 bars, 0.028 of the coin's usual move (12.09 %); normal drift in its direction +0.83 %, total +1.18 %; 4984 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h`
Measure: `measure.py`
