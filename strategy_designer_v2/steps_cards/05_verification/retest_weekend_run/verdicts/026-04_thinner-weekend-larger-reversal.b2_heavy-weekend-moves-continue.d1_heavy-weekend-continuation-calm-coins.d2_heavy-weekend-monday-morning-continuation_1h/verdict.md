---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 12-bar return after Sunday 23:00 forecasts: 0.00534713; t of the mean: 2.65215 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: upper minus lower half of |forecast|, mean signed excess return: 0.00426252, passed: True
- Counts: cases: 463
- Decided by: Mean signed excess 12-bar return above 0 with t >= 2, and the upper |forecast| half beats the lower half.
- Reading: Situation bars are those stamped Sunday 23:00 UTC with the mean volume of the last 48 rows at least the mean of the 120 rows before them (regime used where history is short), side = sign of the 48-row return; the coin's mean 12-bar return is pooled over non-overlapping 12-bar grids of all its windows; upper/lower halves of |forecast| are the top and bottom floor(n/2) cases sorted by |forecast| (the middle case dropped if n is odd); the plan's 'fewer than 200 cases' rule is reported as not observable.
- Size: unusual move +0.67 % per case over 12 bars, 0.186 of the coin's usual move (3.43 %); normal drift in its direction +0.02 %, total +0.69 %; 405 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h`
Measure: `measure.py`
