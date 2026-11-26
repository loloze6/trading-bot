---
plan: 032-02_low-range-decline-continues-more_1d
idea: 032-02_low-range-decline-continues-more
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 5-bar return on abs forecast (trending grid bars): -0.000334468; OLS slope t: -0.729981 (threshold: confirm: slope negative with t <= -2 (and supporting check passes); reject: slope positive with t >= +2)
- Supporting check: abs-forecast-weighted mean drift-adjusted 5-bar return below 0: -0.00353128, passed: True
- Counts: grid cases in the regime: 1648, active bars checked: 6316
- Decided by: The slope's t lies between -2 and +2, the plan's inconclusive rule.
- Reading: Situation check counts only active bars whose 28-day return can be computed from the window's own closes (the first 28 bars of each window are left out), side short when forecast < 0; grid cases are bars at positions 0,5,10,... of each window with regime 'trending', a finite 5-bar forward return inside the window and a recorded calm post_pipeline_value, the coin's drift being the mean 5-bar return over all its windows' grid bars, the slope's t from ordinary least squares, and fewer than 200 cases gives 'not observable'.
- Size: unusual move +0.10 % (t 0.22, the cases of one day together: 588 days) per case over 5 bars, 0.011 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total -0.55 %; 861 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02_low-range-decline-continues-more_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02_low-range-decline-continues-more_1d`
Measure: `measure.py`
