---
plan: 041-01.b1_rising-agitated-rise-continues_1d
idea: 041-01.b1_rising-agitated-rise-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of next-day excess return on forecast, day-clustered: 0.000637477; day-clustered slope t: 1.86062 (threshold: confirm: slope t >= 2 with mean excess > 0; reject: slope t <= -2)
- Supporting check: mean excess next-day return over cases > 0: -0.000441465, passed: False
- Counts: cases: 1273, distinct days: 758
- Decided by: Inconclusive: slope t lies between -2 and 2.
- Reading: The situation is a positive one-day scaled return (the recorded scaled_rise raw value > 0, or the day's close-to-close return > 0 where it is not recorded) on the long side; the horizon of 1 bar makes every bar its own grid cell; the coin's mean daily return pools all its windows' 1-day returns; the regression is OLS with an intercept and day-clustered (CR1) standard errors; the plan's 'fewer than 100 cases on at least 50 distinct days' minimum is reported as not observable, as the workflow requires.
- Size: unusual move +0.12 % (t 0.44, the cases of one day together: 529 days) per case over 1 bars, 0.030 of the coin's usual move (5.25 %); normal drift in its direction +0.11 %, total +0.23 %; 830 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.861 (not below 1), 1273 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/041-01.b1_rising-agitated-rise-continues_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/041-01.b1_rising-agitated-rise-continues_1d`
Measure: `measure.py`
