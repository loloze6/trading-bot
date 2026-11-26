---
plan: 059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation_1d
idea: 059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 14-bar excess return on forecast (grid cases, forecast > 0): 0.00621488; slope t, clustered by day: 2.30226 (threshold: t >= 2 confirms (with top third > 0), t <= -2 rejects)
- Supporting check: mean excess 14-bar return of the top third of forecasts: 0.0442825, passed: True
- Counts: grid cases with a forecast above 0: 180, days of the cases: 79, top third cases: 60
- Decided by: Confirm rule: the slope's t is 2 or more and the top third's mean excess return is above 0.
- Reading: The profile is the regime 'unknown' and the rise a positive raw scaled return; the grid is bars 0, 14, 28, ... of each window with a full 14-bar return; the slope's t uses day-clustered standard errors (CR1); the top third is the ceil(n/3) largest forecasts, its t with deviations summed per day; the minimum of 30 cases is applied first as 'not observable'.
- Size: unusual move +0.12 % (t 0.11, the cases of one day together: 348 days) per case over 14 bars, -0.006 of the coin's usual move (18.92 %); normal drift in its direction +2.23 %, total +2.34 %; 531 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (46 cases, 58 days)
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation_1d`
Measure: `measure.py`
