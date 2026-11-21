---
plan: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h
idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-removed 120-bar short-side move per case: -0.00182754; t of the mean: -0.471624 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: deeper-half minus shallower-half mean move (by |forecast|): 0.0120179, passed: True
- Counts: independent cases: 1186
- Decided by: The main t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Surge recomputed as the 24h return over the mean absolute 24h return of the last 720 bars (the recorded regime label stands in where a window lacks 744 bars of history), prior week from fall_depth's raw value; one case per 120-bar grid cell = the first short bet in that cell; the depth halves are the top and bottom n//2 cases by |forecast| (the middle case dropped when n is odd).
- Size: unusual move -0.18 % per case over 120 bars, -0.008 of the coin's usual move (12.09 %); normal drift in its direction -0.85 %, total -1.03 %; 1186 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h`
Measure: `measure.py`
