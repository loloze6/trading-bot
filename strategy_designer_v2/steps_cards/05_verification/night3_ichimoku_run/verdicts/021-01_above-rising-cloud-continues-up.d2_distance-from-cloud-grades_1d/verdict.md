---
plan: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
idea: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of pooled 26-bar forward excess return (minus coin drift) on forecast: 1.52173; OLS t of slope: 1.52173 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 non-overlapping cases)
- Supporting check: none
- Counts: non-overlapping cases: 576
- Decided by: t = 1.52 lies between -2 and 2 on 576 non-overlapping cases.
- Reading: Ordinary least squares with an intercept, pooled over all coins, on every grid bar with a 26-bar return inside its window (bars with forecast 0 included); drift is the coin's mean of these grid returns over all windows.
- Size: unusual move +0.22 % per case over 26 bars, 0.001 of the coin's usual move (25.48 %); normal drift in its direction -0.87 %, total -0.65 %; 539 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d`
Measure: `measure.py`
