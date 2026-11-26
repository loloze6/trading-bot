---
plan: 031-02.b1.b2.b1_failed-rally-longer-horizon_1d
idea: 031-02.b1.b2.b1_failed-rally-longer-horizon
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x drift-removed 40-bar forward return on grid cases: 0.00554237; t of the mean, cases summed per day: 0.363281 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean drift-removed 40-bar return when forecast <= -2 below 0: -0.130154, passed: True
- Counts: grid cases: 344, grid cases on separate days: 54, cases with forecast <= -2: 30, active bars: 15942
- Decided by: The t is between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: The 60-day return is recomputed from closes inside the window where 60 prior bars exist and taken from the recorded regime (mean_reversion) on earlier bars; the expected side is graded as the Fidelity's comparison says (short when the standardised low proximity is above its usual level 10, long when below, read from low_prox post_pipeline_value since the 365-bar standardise history is not in the record); grid cases are positions 0, 40, 80, ... of each window with a full 40-bar forward return inside the window; the drift is the coin's mean 40-bar return over the same grid of all its windows; the t is clustered by day (deviations summed per day); the plan's 'fewer than 30 grid cases on separate days' is applied as a minimum count of 30 distinct days, reported as not observable; a check with no case at forecast <= -2 counts as failed.
- Size: unusual move -0.74 % (t -0.19, the cases of one day together: 213 days) per case over 40 bars, 0.019 of the coin's usual move (34.25 %); normal drift in its direction +3.95 %, total +3.21 %; 361 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-02.b1.b2.b1_failed-rally-longer-horizon_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b2.b1_failed-rally-longer-horizon_1d`
Measure: `measure.py`
