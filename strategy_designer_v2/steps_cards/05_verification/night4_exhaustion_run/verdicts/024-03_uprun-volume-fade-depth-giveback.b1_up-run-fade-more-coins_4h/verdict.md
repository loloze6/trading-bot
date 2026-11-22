---
plan: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h
idea: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 18-bar return of short cases, sign flipped: 0.00103908; t of the mean: 1.17962 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: OLS coefficient of vol_fade (raw) in drift-adjusted 18-bar return ~ run_gain + vol_fade: -0.00090978, passed: False
- Counts: cases overall: 12138, cases in regression: 12138
- Decided by: Neither the confirm nor the reject rule is met: a result in between.
- Reading: A case is the workflow's short bet (forecast at least 2 points more negative than its least-negative level since the last bet, reset at flat), first one per 18-bar grid cell of each window; the regression uses the unflipped drift-adjusted return with an intercept and classical OLS t; fewer than 30 cases is reported as not observable; the situation is an up-close bar on the short side.
- Size: unusual move +0.10 % per case over 18 bars, 0.011 of the coin's usual move (9.29 %); normal drift in its direction -0.52 %, total -0.42 %; 12138 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h`
Measure: `measure.py`
