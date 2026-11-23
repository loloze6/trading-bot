---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x drift-adjusted 2-bar return over Sunday-close cases: 0.066016; t of the mean: 5.71707 (threshold: confirm: mean > 0 with t >= 2 over >= 200 cases and size check passes; reject: mean < 0 with t <= -2 over >= 200 cases)
- Supporting check: largest third minus smallest third, mean drift-adjusted 2-bar return in forecast direction: 0.00563064, passed: True
- Counts: cases: 5244, smallest third cases: 1748, largest third cases: 1748
- Decided by: The mean forecast-weighted drift-adjusted 2-bar return is positive with t >= 2 over at least 200 cases and the size check passes.
- Reading: The situation is a bar opening on Sunday UTC with forecast sign opposite to its 1-day return (raw value, or close-to-close if missing); cases need a 2-bar return inside the window; each coin's drift is the mean of its non-overlapping 2-bar returns on a grid from each window's first row; thirds are formed by sorting cases by |forecast| (stable order, ties by position) and splitting into three near-equal groups; the size check compares the mean of sign(forecast) x drift-adjusted return, largest third minus smallest third.
- Size: unusual move +0.71 % per case over 2 bars, 0.097 of the coin's usual move (7.48 %); normal drift in its direction +0.01 %, total +0.72 %; 4388 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d`
Measure: `measure.py`
