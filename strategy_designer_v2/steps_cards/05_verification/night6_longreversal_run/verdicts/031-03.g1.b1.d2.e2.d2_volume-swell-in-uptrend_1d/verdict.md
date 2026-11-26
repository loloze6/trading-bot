---
plan: 031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend_1d
idea: 031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 14-bar excess return on forecast, trending grid cases: 0.00271361; day-clustered OLS t of the slope: 1.64755 (threshold: t >= 2 (with supporting check) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean excess 14-bar return of grid cases with forecast > 0 (long): 0.0387239, passed: True
- Counts: grid cases with forecast above 0: 647, trending grid cases: 1166
- Decided by: The slope's t is between -2 and 2.
- Reading: The coin's mean 14-bar return is taken over all its windows' grid bars (every regime), the regime is the recorded one, the day-clustered t uses the usual G/(G-1)*(N-1)/(N-K) correction, and the plan's minimum counts are applied as 'not observable'; in the situation check the 50-day mean comes from the window's closes where 50 bars exist, otherwise from the recorded regime.
- Size: unusual move +2.94 % (t 2.63, the cases of one day together: 593 days) per case over 14 bars, 0.117 of the coin's usual move (20.98 %); normal drift in its direction +2.47 %, total +5.41 %; 944 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend_1d`
Measure: `measure.py`
