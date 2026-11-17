---
plan: 011-01_weekend-rise-reverses-monday_1d
idea: 011-01_weekend-rise-reverses-monday
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean per-case gain (forecast/10) x (2-bar return - m) on Sunday bars with forecast < 0: 0.00645658; ordinary t of the mean: 2.7527 (threshold: confirm: mean gain > 0 with t >= 2 and supporting check passes; reject: mean gain < 0 with t <= -2)
- Supporting check: excess 2-bar return of large-|forecast| half minus small-|forecast| half (< 0 passes): 0.00350037, passed: False
- Counts: cases pooled: 1268, large-forecast half: 634, small-forecast half: 634
- Decided by: t >= 2 but the supporting check fails, which the plan calls inconclusive.
- Reading: Cases are Sunday-stamped (UTC) bars with forecast < 0 that have close[t+2] in the same window; m per coin from the 0,2,4,... grid of each window pooled over all windows; the median split puts |forecast| above the median in the large half and the rest in the small half; the plan's 'fewer than 100 cases' minimum is reported as not observable.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday_1d`
Measure: `measure.py`
