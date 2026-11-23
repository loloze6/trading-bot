---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean signed excess 2-bar move after Sunday forecasts: 0.00974168; ordinary t of the mean: 5.46269 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: mean signed excess, larger |forecast| half minus smaller half: 0.0170778, passed: True
- Counts: cases: 2194, larger half: 1097, smaller half: 1097
- Decided by: Mean signed excess move positive with t >= 2 over at least 100 cases, and the larger-|forecast| half beats the smaller half.
- Reading: A Sunday bar is the daily bar opening on Sunday UTC (its close is Sunday's close); the volatility ratio is recomputed from closes inside each window as rolling std (ddof 1) of 20 over 60 one-bar returns including the bar, and active bars where it cannot be computed (first 60 bars of a window) are left out of the agreement; the drift is each coin's mean 2-bar return on the grid 0,2,4,... of every window pooled; for the supporting check the larger half is |forecast| strictly above the median and the smaller half at or below it; fewer than 100 cases gives 'not observable' as the workflow requires.
- Size: unusual move +1.08 % per case over 2 bars, 0.143 of the coin's usual move (7.48 %); normal drift in its direction -0.00 %, total +1.08 %; 1935 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d`
Measure: `measure.py`
