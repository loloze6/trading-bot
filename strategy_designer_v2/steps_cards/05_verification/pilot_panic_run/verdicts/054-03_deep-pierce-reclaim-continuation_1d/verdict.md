---
plan: 054-03_deep-pierce-reclaim-continuation_1d
idea: 054-03_deep-pierce-reclaim-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move per case, short direction (fall positive): -0.017197; t of the mean, cases summed per day: -0.914176 (threshold: t >= 2 on a fall to confirm (with supporting check); t <= -2 on a rise to reject)
- Supporting check: abs(post_pipeline_value)-weighted mean unusual move >= equal-weighted mean: -0.0177312, passed: False
- Counts: cases: 66, days: 42
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Situation checked on the pierce-and-reclaim rule only (recorded pierce raw value > 0, else recomputed from prices; the profile is added by code), side short; a case is a short bet (forecast rising by at least 2 points on the short side from its lowest level since the last bet), the first per 5-bar grid cell of each window, with the 5-bar return inside the window; normal drift is the coin's mean 5-bar return on the non-overlapping grid of all its windows; t uses deviations summed per day (clustered by day, G/(G-1) correction); the weight falls back to abs(forecast) if post_pipeline_value is missing.
- Size: unusual move -1.72 % (t -0.93, the cases of one day together: 42 days) per case over 5 bars, -0.119 of the coin's usual move (10.60 %); normal drift in its direction -0.62 %, total -2.34 %; 66 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-03_deep-pierce-reclaim-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-03_deep-pierce-reclaim-continuation_1d`
Measure: `measure.py`
