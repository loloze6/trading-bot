---
plan: 060-01_volume-shrink-fall-continues_1d
idea: 060-01_volume-shrink-fall-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 5-bar forward return on forecast (in-profile grid bars): 0.00147124; day-clustered t of slope: 2.23111 (threshold: confirm: slope > 0 with day-clustered t >= 2 and check < 0; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 5-bar return, forecast <= -2 minus in-profile forecast == 0: -0.0155412, passed: True
- Counts: in-profile grid bars: 1255, grid bars with forecast <= -2: 647, distinct days of forecast <= -2 cases: 259, in-profile grid bars with forecast 0: 535, distinct days of in-profile grid bars: 384
- Decided by: Confirm: the slope is positive with t >= 2 and the supporting difference is below 0.
- Reading: The falling profile is the recorded regime 'unknown'; the grid is positions 0,5,10,... of each window keeping bars with a 5-bar return inside the window; the coin's mean 5-bar return is over all its grid bars in all windows; the slope is OLS with intercept and a CR1 day-clustered t; the 20-distinct-days minimum is read on the forecast <= -2 cases.
- Size: unusual move +0.72 % (t 1.46, the cases of one day together: 400 days) per case over 5 bars, 0.067 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.13 %; 535 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.000153 on the check folds against +0.001471 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-01_volume-shrink-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-01_volume-shrink-fall-continues_1d`
Measure: `measure.py`
