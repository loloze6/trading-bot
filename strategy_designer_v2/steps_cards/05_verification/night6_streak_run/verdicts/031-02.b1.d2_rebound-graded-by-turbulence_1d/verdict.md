---
plan: 031-02.b1.d2_rebound-graded-by-turbulence_1d
idea: 031-02.b1.d2_rebound-graded-by-turbulence
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 2-bar return on forecast, grid bars with forecast > 0: 0.00060665; slope t, day-clustered: 2.77743 (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2)
- Supporting check: mean excess 2-bar return on forecast > 0 grid bars: 0.000729764, passed: True
- Counts: grid bars with forecast > 0: 4217, distinct days: 1125
- Decided by: Confirm: the slope's t is 2 or more and the mean excess 2-bar return on forecast > 0 bars is above 0.
- Reading: Situation = bars whose raw component value (or its recomputation from prices when missing) is > 0 on a down close, long side; grid = rows 0,2,4,... of each window; the coin's mean 2-bar return is the mean over all its windows' grid returns; the slope's t uses a day-clustered standard error (per-day sums of the score, factor G/(G-1)); the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.12 % (t 0.72, the cases of one day together: 1638 days) per case over 2 bars, 0.018 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.36 %; 5188 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.d2_rebound-graded-by-turbulence_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.d2_rebound-graded-by-turbulence_1d`
Measure: `measure.py`
