---
plan: 054-04_weak-reclaim-low-continuation_1d
idea: 054-04_weak-reclaim-low-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move of the short cases, short direction: -0.021561; t of the mean, cases of one day taken together: -1.19535 (threshold: confirm: mean > 0 with t >= 2 and positive nearness slope; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: slope of short-direction unusual move on raw nearness: -0.0835845, passed: False
- Counts: cases: 82, distinct case days: 53, active bars: 104
- Decided by: The t of the mean unusual move lies between -2 and 2 (or cannot be computed), meeting neither the confirm nor the reject rule.
- Reading: Profile taken from the recorded regime 'mean_reversion' (the detector's 365-bar volatility percentile cannot be rebuilt from the window bars), pierce-and-reclaim recomputed from prices where 30 prior bars exist in the window and otherwise from a raw nearness in (0,1]; a case is the first short bet in each 5-bar grid cell of its window with a full 5-bar return inside the window; the minimum of 30 cases on distinct days is treated as a minimum count giving 'not observable'; the day-clustered t uses a small-sample factor D/(D-1).
- Size: unusual move -2.16 % (t -1.21, the cases of one day together: 53 days) per case over 5 bars, -0.202 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -2.79 %; 82 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-04_weak-reclaim-low-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-04_weak-reclaim-low-continuation_1d`
Measure: `measure.py`
