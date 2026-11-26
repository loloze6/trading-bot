---
plan: 072-01.b1_choppy-deep-close-five-day_1d
idea: 072-01.b1_choppy-deep-close-five-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return on forecast (grid cells with forecast < 0): 0.000569626; OLS slope t: 1.08172 (threshold: confirm: slope t >= 2 with supporting check; reject: slope t <= -2)
- Supporting check: mean 5-bar excess return, deepest third minus shallowest third of forecasts (must be < 0): -0.00964653, passed: True
- Counts: grid cases with a nonzero forecast: 819, distinct days: 374
- Decided by: Slope t lies between -2 and 2: inconclusive rule.
- Reading: Choppy profile read as the bars where regime is the config's active regime 'unknown' (|60-day trend| <= 10, the depth component's regime), situation as depth raw value < 0 there; normal drift is the coin's mean 5-bar return on all grid cells of all its windows; slope from pooled OLS over all coins; thirds are the lowest and highest n//3 forecasts by rank; the plan's minimum counts, if not reached, give 'not observable'.
- Size: unusual move +0.43 % (t 1.35, the cases of one day together: 734 days) per case over 5 bars, 0.051 of the coin's usual move (10.60 %); normal drift in its direction -0.57 %, total -0.14 %; 1028 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-01.b1_choppy-deep-close-five-day_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-01.b1_choppy-deep-close-five-day_1d`
Measure: `measure.py`
