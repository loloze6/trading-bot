---
plan: 038-01_rising-market-scaled-rally-continuation_1d
idea: 038-01_rising-market-scaled-rally-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar forward return on forecast (rising-profile grid bars): 0.00108808; OLS t of slope: 3.88345 (threshold: confirm: slope > 0 with t >= 2 and mean unusual move > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean unusual move (strength) of long cases: 0.0358916, passed: True
- Counts: grid cases with forecast > 0: 1273, grid cases in rising profile: 2224, supporting check cases: 1414
- Decided by: The slope is positive with t >= 2 and the mean unusual move of the forecast > 0 cases is above 0.
- Reading: Rising profile read as regime not 'chop'; excess return uses the coin's mean 3-bar return on the non-overlapping grid of all its windows; supporting-check cases are the workflow's long bets (forecast rise >= 2 points from its lowest level since the last bet), one per 3-bar grid cell, strength = (return - drift) / the coin's 3-bar std; the plan's 'fewer than 100 is inconclusive' minimum is reported as 'not observable' per the workflow.
- Size: unusual move +0.30 % (t 0.90, the cases of one day together: 766 days) per case over 3 bars, 0.036 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.67 %; 1414 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0004702 on the check folds against +0.001088 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/038-01_rising-market-scaled-rally-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/038-01_rising-market-scaled-rally-continuation_1d`
Measure: `measure.py`
