---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean signed excess 2-bar move after Sunday forecasts: 0.0072598; ordinary t of the mean: 4.76479 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: mean signed excess, larger |forecast| half minus smaller half: 0.0137798, passed: True
- Counts: cases: 3261, larger half: 1630, smaller half: 1631
- Decided by: Mean signed excess move positive with t >= 2 over at least 100 cases, and the larger-|forecast| half beats the smaller half.
- Reading: A Sunday bar is the daily bar opening on Sunday UTC (its close is Sunday's close); the volatility ratio is recomputed from closes inside each window as rolling std (ddof 1) of 20 over 60 one-bar returns including the bar, and active bars where it cannot be computed (first 60 bars of a window) are left out of the agreement; the drift is each coin's mean 2-bar return on the grid 0,2,4,... of every window pooled; for the supporting check the larger half is |forecast| strictly above the median and the smaller half at or below it; fewer than 100 cases gives 'not observable' as the workflow requires.
- Size: unusual move +0.89 % (t 2.77, the cases of one day together: 448 days) per case over 2 bars, 0.114 of the coin's usual move (7.64 %); normal drift in its direction +0.00 %, total +0.89 %; 2877 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/common/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d`
Measure: `measure.py`
