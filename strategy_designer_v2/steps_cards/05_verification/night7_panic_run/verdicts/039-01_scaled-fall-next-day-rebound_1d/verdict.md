---
plan: 039-01_scaled-fall-next-day-rebound_1d
idea: 039-01_scaled-fall-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (forecast > 0): 0.000397677; slope t, residuals summed per day (day-clustered): 2.62617 (threshold: confirm if t >= 2 (with top-fifth mean > 0); reject if t <= -2)
- Supporting check: mean next-day excess return, top fifth of forecast by coin: 0.00574096, passed: True
- Counts: down-day cases: 8514, distinct days: 2199, top-fifth cases: 1706
- Decided by: Confirm: the slope's t is 2 or more and the top-fifth mean excess return is above 0.
- Reading: Excess = next-day close-to-close return minus the coin's mean 1-day return over all its windows; the slope's t uses day-clustered standard errors (each day's score summed across coins); the top fifth is the coin's cases with forecast at or above its 80th percentile, pooled across coins; a 'down-day case' is a bar with forecast > 0 and a next-day return in the same window.
- Size: unusual move +0.18 % (t 1.45, the cases of one day together: 1702 days) per case over 1 bars, 0.038 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.30 %; 5636 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002362 on the check folds against +0.0003977 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/039-01_scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/039-01_scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
