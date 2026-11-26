---
plan: 067-01.b1_choppy-down-stretch-keeps-falling_1d
idea: 067-01.b1_choppy-down-stretch-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast (grid bars, forecast < 0): -0.000391604; OLS slope t: -0.558758 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2, otherwise inconclusive)
- Supporting check: mean unusual move of bets in short direction: 0.00596321, passed: True
- Counts: grid cases with forecast < 0: 405, bets (cases): 605, days of bets: 449
- Decided by: The slope's t lies between -2 and 2.
- Reading: The drift is each coin's mean non-overlapping 5-bar return over all its windows, the slope's t is the OLS t pooled over coins and windows, the supporting check's cases are the short bets (forecast deepening by >= 2 points) taken once per 5-bar grid cell with the mean over cases, and the plan's 'fewer than 100 grid cases' minimum is applied as not observable.
- Size: unusual move +0.60 % (t 1.50, the cases of one day together: 449 days) per case over 5 bars, 0.071 of the coin's usual move (10.60 %); normal drift in its direction -0.57 %, total +0.03 %; 605 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01.b1_choppy-down-stretch-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1_choppy-down-stretch-keeps-falling_1d`
Measure: `measure.py`
