---
plan: 032-01_monthly-low-break-cascade_1d
idea: 032-01_monthly-low-break-cascade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 3-bar unusual move in the short direction (return minus normal drift, sign flipped): -0.0219867; t of the mean, cases pooled by day: -1.97277 (threshold: confirm: mean > 0 with day-pooled t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of 3-bar return on post_pipeline_value, t >= 1 and positive: 0.218978, passed: False
- Counts: cases: 163, distinct days: 86
- Decided by: Inconclusive: the day-pooled t of the unusual move lies between -2 and 2.
- Reading: The profile part of the situation is read from the recorded regime ('trending' is only reachable past the falling/agitated vetoes, whose components are not recorded), the break from break_depth's last_history_value < 0 (recomputed from the window's prior 30 closes where missing); a case is the first short bet (forecast rising in size on the short side by at least 2 points) in each 3-bar grid cell of a window, measured from that bet bar's close over 3 bars; the coin's normal drift is the mean of its non-overlapping 3-bar returns on the same grid over all its windows; the supporting slope is an OLS of the raw 3-bar return on post_pipeline_value with its ordinary t; the plan's 30 cases on 30 distinct days are treated as minimum counts (not observable if unmet).
- Size: unusual move -2.20 % (t -1.98, the cases of one day together: 86 days) per case over 3 bars, -0.269 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total -2.59 %; 163 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/032-01_monthly-low-break-cascade_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/032-01_monthly-low-break-cascade_1d`
Measure: `measure.py`
