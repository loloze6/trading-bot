---
plan: 040-01_rising-swing-scaled-weeks-rise-continues_1d
idea: 040-01_rising-swing-scaled-weeks-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 14-bar excess return on forecast (forecast > 0, in profile, 14-bar grid): 0.0026084; t of slope (day-clustered): 1.1263 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 14-bar return of forecast > 0 cases > 0: 0.017443, passed: True
- Counts: grid cases with forecast > 0: 662, distinct days: 132
- Decided by: The slope's |t| is below 2.
- Reading: Rising profile read as regime == 'unknown' (the 60-day price-evolution veto not firing), the situation as profile bars with the raw 20-day swing-scaled return > 0 on the long side; the coin's mean 14-bar return is taken over all its non-overlapping grid cases in all windows; the slope's t uses day-clustered errors (each day's x-deviation times residual summed per day); days are the UTC dates of the case bars.
- Size: unusual move +2.05 % (t 1.91, the cases of one day together: 520 days) per case over 14 bars, 0.095 of the coin's usual move (20.98 %); normal drift in its direction +2.52 %, total +4.57 %; 1005 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/040-01_rising-swing-scaled-weeks-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/040-01_rising-swing-scaled-weeks-rise-continues_1d`
Measure: `measure.py`
