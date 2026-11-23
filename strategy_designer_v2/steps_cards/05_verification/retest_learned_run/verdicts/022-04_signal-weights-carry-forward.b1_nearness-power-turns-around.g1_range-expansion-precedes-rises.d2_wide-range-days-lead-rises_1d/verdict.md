---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar return on forecast (forecast > 0 grid cases, pooled): 1.00784e-05; OLS slope t: 0.0228955 (threshold: slope t >= 2 confirms (with mean excess t >= 1 and >= 200 cases); slope t <= -2 rejects)
- Supporting check: mean excess 5-bar return of the same cases, ordinary t >= 1: 2.2871, passed: True
- Counts: grid cases with forecast > 0: 1370
- Decided by: Slope t between -2 and 2: inconclusive per the plan.
- Reading: Grid per window at positions 0,5,10,... with the 5-bar return inside the window; normal drift = mean 5-bar return over all grid cells of all the coin's windows; the plan's 'fewer than 200 cases' rule is reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +0.53 % per case over 5 bars, 0.044 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +1.12 %; 2353 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises_1d`
Measure: `measure.py`
