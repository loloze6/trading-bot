---
plan: 013-02_follow-through-stronger-near-high_1d
idea: 013-02_follow-through-stronger-near-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess forward 30-bar return on forecast/10: 0.00207032; OLS slope t: 0.130658 (threshold: main slope t >= +2 confirms (with near-minus-far slope difference > 0); t <= -2 rejects; at least 300 independent grid cases)
- Supporting check: slope of excess forward return on past return, above-median W minus below-median W: 0.181469, passed: True
- Counts: independent grid cases: 526, above-median W cases: 193, below-median W cases: 193
- Decided by: The main slope's t lies between -2 and +2.
- Reading: Grid positions 0/30/60/90 are used only where the bar 30 rows later exists in the same window; the coin mean is the mean of that coin's grid forward returns over all windows; the regression has an intercept; the median split is pooled over all coins, with cases exactly at the median left out.
- Size: unusual move +2.77 % per case over 30 bars, 0.095 of the coin's usual move (25.51 %); normal drift in its direction +0.91 %, total +3.69 %; 264 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-02_follow-through-stronger-near-high_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-02_follow-through-stronger-near-high_1d`
Measure: `measure.py`
