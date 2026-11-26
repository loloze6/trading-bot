---
plan: 067-01_choppy-up-stretch-keeps-rising_1d
idea: 067-01_choppy-up-stretch-keeps-rising
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar excess return on forecast (grid, active bars): 0.000566707; slope t, cases summed by date: 0.72738 (threshold: t >= 2 (with both sides' mean positive) confirms; t <= -2 rejects)
- Supporting check: mean excess return in forecast direction, long and short sides: -0.00350174, passed: False
- Counts: grid cases in total: 408, long cases: 208, short cases: 200, dates: 187
- Decided by: The slope's t is between -2 and 2.
- Reading: Choppy bars are bars whose recorded regime is not the veto regime 'chop' (the profile's trend gate, whose component is not recorded); the stretch's side is the sign of the raw stretch, or of close minus its 20-bar SMA when the raw value is missing; the drift is the mean next-10-bar return over every grid bar of all the coin's windows; the slope t uses an OLS slope with a standard error clustered by date (residual-weighted deviations summed per date, G/(G-1) correction); the plan's 'fewer than 100 / 30' rule is treated as a minimum count (not observable).
- Size: unusual move -0.05 % (t -0.09, the cases of one day together: 536 days) per case over 10 bars, -0.016 of the coin's usual move (14.49 %); normal drift in its direction +0.01 %, total -0.04 %; 717 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01_choppy-up-stretch-keeps-rising_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01_choppy-up-stretch-keeps-rising_1d`
Measure: `measure.py`
