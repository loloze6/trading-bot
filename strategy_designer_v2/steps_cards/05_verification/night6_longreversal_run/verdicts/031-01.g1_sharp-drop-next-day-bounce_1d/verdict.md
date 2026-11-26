---
plan: 031-01.g1_sharp-drop-next-day-bounce_1d
idea: 031-01.g1_sharp-drop-next-day-bounce
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-bar excess return on forecast (forecast > 0 bars): 0.000397677; day-clustered t of slope: 2.62617 (threshold: slope > 0 with day-clustered t >= 2 confirms (with check); slope < 0 with t <= -2 rejects)
- Supporting check: forecast-weighted mean next-bar excess return, day-clustered t: 0.00349831, passed: True
- Counts: bars with forecast > 0: 8514, distinct days: 2199
- Decided by: Confirm: the slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0 with t >= 2.
- Reading: Every bar with forecast > 0 and a next bar in the same window is used; the coin's mean is the mean next-bar return over all its windows; clustered standard errors use the CR1 sandwich with the G/(G-1)*(N-1)/(N-K) correction; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.18 % (t 1.45, the cases of one day together: 1702 days) per case over 1 bars, 0.038 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.30 %; 5636 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-01.g1_sharp-drop-next-day-bounce_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-01.g1_sharp-drop-next-day-bounce_1d`
Measure: `measure.py`
