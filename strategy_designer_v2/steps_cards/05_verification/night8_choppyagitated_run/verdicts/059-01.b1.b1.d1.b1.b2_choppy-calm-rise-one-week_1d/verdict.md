---
plan: 059-01.b1.b1.d1.b1.b2_choppy-calm-rise-one-week_1d
idea: 059-01.b1.b1.d1.b1.b2_choppy-calm-rise-one-week
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day t of the slope of next-7-bar excess return on forecast (forecast > 0, 7-bar grid): 2.47501; OLS slope t, standard errors clustered by day: 2.47501 (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2, or mean excess < 0 with t <= -2)
- Supporting check: mean excess 7-bar return over cases with forecast > 0: 0.00173927, passed: True
- Counts: grid cases with forecast > 0: 409, distinct days: 163
- Decided by: Confirm rule met: the slope's t is 2 or more and the mean excess return is above 0.
- Reading: The slope is from an OLS with intercept whose t uses day-clustered (CR1) standard errors, the normal drift is each coin's mean 7-bar return on the non-overlapping grid of all its windows, the reject rule's mean-excess t is the day-clustered t of the mean, and the plan's 'inconclusive with too few cases' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.38 % (t 0.66, the cases of one day together: 492 days) per case over 7 bars, 0.023 of the coin's usual move (12.84 %); normal drift in its direction +0.95 %, total +1.33 %; 793 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +1.375 on the check folds against +2.475 on every fold
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b2_choppy-calm-rise-one-week_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b2_choppy-calm-rise-one-week_1d`
Measure: `measure.py`
