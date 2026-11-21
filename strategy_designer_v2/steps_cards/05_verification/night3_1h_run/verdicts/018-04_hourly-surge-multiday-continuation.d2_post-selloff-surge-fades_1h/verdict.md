---
plan: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 120-bar shortfall vs normal drift, short direction, before costs: 0.00321515; t of the mean: 0.743794 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases)
- Supporting check: slope of shortfall on absolute forecast (fall depth): 0.000462894, passed: True
- Counts: cases: 559
- Decided by: The t of the mean shortfall lies between -2 and 2.
- Reading: Surge is recomputed from closes as the 24-bar return over the mean absolute 24-bar return of the last 720 bars inside the window, prior7 is the recorded fall_depth raw value (same component and parameters) or its price recomputation, active bars where surge cannot be computed are left out of the agreement; a case is the first short bet (forecast falling at least 2 points below its least-negative level since the last bet, reset at flat) in each 120-bar grid cell of a window, cases are pooled over all coins, the drift is each coin's mean non-overlapping 120-bar return over all its windows, the slope is an OLS slope of shortfall on |forecast|, and fewer than 30 cases is 'not observable'.
- Size: unusual move +0.32 % per case over 120 bars, 0.033 of the coin's usual move (10.37 %); normal drift in its direction -0.65 %, total -0.33 %; 559 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h`
Measure: `measure.py`
