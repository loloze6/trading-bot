---
plan: 016-03_up-jump-price-reversal_1h
idea: 016-03_up-jump-price-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess next-72-bar return on forecast (trending grid bars): 0.000968346; OLS t of slope: 2.73615 (threshold: confirm: slope > 0 with t >= 2 (and supporting slope > 0); reject: slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: OLS slope of giveback fraction on |forecast|: 0.0516392, passed: True
- Counts: grid cases: 2916, giveback cases: 2865
- Decided by: Main slope positive with t >= 2 and the supporting giveback slope positive (confirm rule).
- Reading: Situation computed as close[t]/close[t-72]-1 > 0 inside each window (falling back to regime == 'trending' on the first 72 bars of a window where the past is not recorded) with short side forecast < 0; grid is positions 0,72,144,... of each window, a coin's mean grid return pools all its grid bars with a forward return across windows, the giveback needs close[t-72] inside the window, and the plan's 'below 100 cases inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.05 % per case over 72 bars, 0.005 of the coin's usual move (8.23 %); normal drift in its direction -0.41 %, total -0.36 %; 4896 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-03_up-jump-price-reversal_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-03_up-jump-price-reversal_1h`
Measure: `measure.py`
