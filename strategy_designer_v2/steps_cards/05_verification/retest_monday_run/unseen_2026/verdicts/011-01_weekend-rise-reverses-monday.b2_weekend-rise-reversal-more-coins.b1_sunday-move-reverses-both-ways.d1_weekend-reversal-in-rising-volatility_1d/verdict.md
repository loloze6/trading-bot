---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean signed excess 2-bar move after Sunday forecasts: -0.00351404; ordinary t of the mean: -1.20665 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: mean signed excess, larger |forecast| half minus smaller half: 0.00120354, passed: True
- Counts: cases: 346, larger half: 173, smaller half: 173
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A Sunday bar is the daily bar opening on Sunday UTC (its close is Sunday's close); the volatility ratio is recomputed from closes inside each window as rolling std (ddof 1) of 20 over 60 one-bar returns including the bar, and active bars where it cannot be computed (first 60 bars of a window) are left out of the agreement; the drift is each coin's mean 2-bar return on the grid 0,2,4,... of every window pooled; for the supporting check the larger half is |forecast| strictly above the median and the smaller half at or below it; fewer than 100 cases gives 'not observable' as the workflow requires.
- Size: unusual move -0.46 % per case over 2 bars, -0.082 of the coin's usual move (5.76 %); normal drift in its direction -0.01 %, total -0.47 %; 305 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/unseen_2026/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d`
Measure: `measure.py`
