---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 3-bar return after Sunday falls: 0.013424; ordinary t of the mean of forecast-scaled excess returns: 4.95412 (threshold: confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2)
- Supporting check: least-squares slope of excess 3-bar return on forecast > 0: 0.00138219, passed: True
- Counts: cases: 2173
- Decided by: Confirm: weighted mean excess 3-bar return above 0 with t >= 2 and a positive slope on the forecast.
- Reading: Every Sunday bar (UTC start on Sunday) in regime mean_reversion with forecast >= 2 and three later bars in its window is one case (Sundays are 7 bars apart, so their 3-bar returns never overlap), and the coin's drift is the mean of its 3-bar returns on the grid 0, 3, 6, ... of each window, pooled over all its windows.
- Size: unusual move +0.90 % per case over 3 bars, 0.105 of the coin's usual move (9.14 %); normal drift in its direction +0.47 %, total +1.36 %; 2174 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d`
Measure: `measure.py`
