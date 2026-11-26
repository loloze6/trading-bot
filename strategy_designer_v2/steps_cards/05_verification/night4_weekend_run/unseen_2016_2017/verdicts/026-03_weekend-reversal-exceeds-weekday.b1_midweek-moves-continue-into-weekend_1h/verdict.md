---
plan: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed 48-bar return on forecast, Thursday-23:00 cases: -0.000964696; OLS slope t: -1.99642 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2; at least 300 cases)
- Supporting check: mean drift-removed 48-bar return in the forecast's direction: -0.0149293, passed: False
- Counts: cases: 312, active bars: 319, situation bars with non-zero forecast: 317
- Decided by: The slope's t is between -2 and 2.
- Reading: Cases are bars starting Thursday 23:00 UTC with a non-zero forecast and a full 48-bar forward return inside their window; the normal drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; the fit has an intercept; fewer than 300 cases is reported as not observable.
- Size: unusual move -1.42 % (t -1.65, the cases of one day together: 100 days) per case over 48 bars, -0.110 of the coin's usual move (13.44 %); normal drift in its direction +0.15 %, total -1.26 %; 273 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2016_2017/backtests/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h`
Measure: `measure.py`
