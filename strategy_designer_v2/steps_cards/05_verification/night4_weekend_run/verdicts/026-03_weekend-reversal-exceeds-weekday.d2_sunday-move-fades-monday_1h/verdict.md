---
plan: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-24-bar return minus coin drift on the Monday 00:00 forecast: 0.000238095; t of the OLS slope: 2.56537 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean of sign(forecast) x (next-24-bar return minus drift): 0.00384283, passed: True
- Counts: Monday cases with a nonzero forecast: 2435
- Decided by: The slope is positive with t >= 2 and the supporting mean is above 0.
- Reading: Situation bars are the bars starting Sunday 23:00 UTC (closing Monday 00:00), Sunday's return is the recorded raw component value (recomputed from 24-row prices where missing), the regression is ordinary least squares with an intercept, the drift is each coin's mean 24-bar return on the 0, 24, 48, ... row grid of all its windows, and fewer than 300 cases is reported as not observable as the instructions require.
- Size: unusual move +0.40 % per case over 24 bars, 0.081 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.39 %; 2155 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h`
Measure: `measure.py`
