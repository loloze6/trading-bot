---
plan: 058-03.b1_calm-rise-continuation-all-coins_1d
idea: 058-03.b1_calm-rise-continuation-all-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return (vs coin's mean 5-bar return) on forecast, grid bars with forecast > 0: 0.00174682; slope t, clustered by day: 2.06337 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases with forecast above 0: 750, distinct days: 234
- Decided by: Confirm rule met: the slope is positive with t >= 2.
- Reading: The coin's mean 5-bar return is the mean over the same non-overlapping 5-bar grid of all its windows; the slope's t uses an OLS with intercept and standard errors clustered by UTC day of the signal bar (CR1 small-sample correction); the plan's 'fewer than 100 cases or 30 days' rule is applied as the minimum counts (status 'not observable').
- Size: unusual move +0.41 % (t 0.67, the cases of one day together: 487 days) per case over 5 bars, 0.043 of the coin's usual move (11.68 %); normal drift in its direction +0.73 %, total +1.14 %; 866 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.002415 on the check folds against +0.001747 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.b1_calm-rise-continuation-all-coins_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03.b1_calm-rise-continuation-all-coins_1d`
Measure: `measure.py`
