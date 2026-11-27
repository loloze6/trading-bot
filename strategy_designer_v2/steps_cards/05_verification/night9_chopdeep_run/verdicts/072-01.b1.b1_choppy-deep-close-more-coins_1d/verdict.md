---
plan: 072-01.b1.b1_choppy-deep-close-more-coins_1d
idea: 072-01.b1.b1_choppy-deep-close-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess forward return on forecast (non-overlapping grid, active bars): 0.000587973; OLS slope t, clustered by day: 0.693735 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2 (t clustered by day))
- Supporting check: deepest minus shallowest third by |forecast|, mean excess 5-bar return (Welch t <= -2): -0.0117625, passed: False
- Counts: grid cases: 1640, distinct days: 429, deepest third cases: 547, shallowest third cases: 547
- Decided by: The slope's |t| is below 2 (or undefined): neither confirm nor reject, so inconclusive.
- Reading: The choppy profile is read as the bars whose recorded regime is 'unknown' (the only regime with a strategy, i.e. 60-bar price evolution between -10 and +10), the situation as a close below its 20-day high (depth < 0) on the short side; the drift is the coin's mean non-overlapping 5-bar return over all its windows' grids, the slope's t is clustered by calendar day (UTC), and thirds are cut by rank of |forecast| over all grid cases.
- Size: unusual move +0.45 % (t 1.35, the cases of one day together: 1112 days) per case over 5 bars, 0.041 of the coin's usual move (12.35 %); normal drift in its direction -0.79 %, total -0.34 %; 2159 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-01.b1.b1_choppy-deep-close-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-01.b1.b1_choppy-deep-close-more-coins_1d`
Measure: `measure.py`
