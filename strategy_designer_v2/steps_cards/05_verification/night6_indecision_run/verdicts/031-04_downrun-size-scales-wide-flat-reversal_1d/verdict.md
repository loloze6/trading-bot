---
plan: 031-04_downrun-size-scales-wide-flat-reversal_1d
idea: 031-04_downrun-size-scales-wide-flat-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar forward excess return on forecast, mean_reversion bars: -0.00114447; slope t, residual scores summed per day: -0.550279 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean 5-bar excess return of cases with forecast >= 2 above 0: -0.00998832, passed: False
- Counts: independent cases: 130, cases with forecast >= 2: 41, days with cases: 108
- Decided by: The slope's |t| is below 2 (or its sign disagrees with t), which the plan calls inconclusive.
- Reading: Cases are mean_reversion bars with a 5-bar forward return inside their window, kept greedily so that a case 1 to 5 bars after a kept case is dropped; the coin's mean 5-bar return is taken on the non-overlapping grid (positions 0, 5, 10, ...) of all its windows; the day-summed t uses the OLS residual scores clustered by UTC day with a G/(G-1) correction; the plan's minimum counts give 'not observable' when not reached.
- Size: unusual move -1.28 % (t -0.55, the cases of one day together: 33 days) per case over 5 bars, -0.171 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total -0.70 %; 43 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-04_downrun-size-scales-wide-flat-reversal_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-04_downrun-size-scales-wide-flat-reversal_1d`
Measure: `measure.py`
