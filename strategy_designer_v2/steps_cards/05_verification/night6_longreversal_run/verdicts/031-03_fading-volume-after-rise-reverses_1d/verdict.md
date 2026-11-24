---
plan: 031-03_fading-volume-after-rise-reverses_1d
idea: 031-03_fading-volume-after-rise-reverses
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 30-day excess return on forecast, regime grid bars: -0.00759707; OLS slope t: -0.463898 (threshold: confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; else inconclusive)
- Supporting check: mean excess 30-day return on forecast <= -2 cases below 0: 0.0607317, passed: False
- Counts: regime grid cases: 57, short-bet cases (forecast <= -2): 16
- Decided by: The slope's |t| is below 2.0.
- Reading: The rise regime is read from the recorded `regime` column (the detector's 90-day/365-day component is not recorded and its 455-bar history cannot be rebuilt inside a window), the volume drop from vol_drop's raw value below 0, the expected side short; regime grid cases include bars with forecast 0; the coin's mean 30-day return is taken over the 30-bar grid of all its windows; the plan's 'fewer than 30 regime grid cases' is applied as a minimum count (not observable).
- Size: unusual move -2.79 % (t -0.69, the cases of one day together: 45 days) per case over 30 bars, -0.116 of the coin's usual move (25.51 %); normal drift in its direction -3.67 %, total -6.46 %; 55 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03_fading-volume-after-rise-reverses_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03_fading-volume-after-rise-reverses_1d`
Measure: `measure.py`
