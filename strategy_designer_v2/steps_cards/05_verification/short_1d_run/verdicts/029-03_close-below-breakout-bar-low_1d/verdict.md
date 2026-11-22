---
plan: 029-03_close-below-breakout-bar-low_1d
idea: 029-03_close-below-breakout-bar-low
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after forecast < 0 (non-overlapping grid): -0.0282495; t of the mean: -1.61879 (threshold: confirm: mean < 0 with t <= -2 over >= 30 cases and rank correlation < 0; reject: mean > 0 with t >= +2 over >= 30 cases)
- Supporting check: Spearman rank correlation of |forecast| with excess 5-bar return, below 0: None, passed: False
- Counts: cases: 18, active bars: 63
- Decided by: Only 18 cases, all coins and windows pooled, fewer than the plan's minimum of 30.
- Reading: Situation bars are bars with the recorded raw fail_depth value above 0 (recomputed from prices only where missing); grid bars whose 5-bar forward return would leave the window are dropped both from the cases and from the coin's mean, and an undefined rank correlation counts as a failed check.
- Size: unusual move +2.83 % per case over 5 bars, 0.254 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +2.24 %; 50 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-03_close-below-breakout-bar-low_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-03_close-below-breakout-bar-low_1d`
Measure: `measure.py`
