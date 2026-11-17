---
plan: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of (forecast/10) x (r2 - m2) on Sunday-close active bars: 0.00429027; ordinary t of the mean: 2.75089 (threshold: confirm: mean > 0 with t >= 2.0 and supporting check > 0; reject: mean < 0 with t <= -2.0; at least 300 Sunday cases)
- Supporting check: mean of -sign(weekend move) x (r2 - m2), top half of |forecast| minus bottom half: -0.000842908, passed: False
- Counts: Sunday cases: 2464, larger |forecast| half: 1232, smaller |forecast| half: 1232
- Decided by: t >= 2.0 but the supporting check is at or below 0 (or not computable), which the plan calls inconclusive.
- Reading: Cases are bars starting on Sunday (UTC) with non-zero forecast and close[t+2] in the same window; m2 is each coin's mean 2-bar return on the grid 0,2,4,... of every window pooled over windows; the median split puts |forecast| above the median in the larger half and the rest in the smaller half; weekend move sign is the sign of the raw component value.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d`
Measure: `measure.py`
