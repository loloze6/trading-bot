---
plan: 038-01_agitated-fall-next-day-rebound_1d
idea: 038-01_agitated-fall-next-day-rebound
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (return per forecast point): 0.00179144; t clustered by day: 0.737809 (threshold: confirm: slope > 0 with t >= 2 and weighted mean > 0; reject: slope < 0 with t <= -2; min 100 cases on 60 distinct days)
- Supporting check: forecast-weighted mean next-day excess return above 0: 0.00554824, passed: True
- Counts: cases: 19, distinct days: 19
- Decided by: The plan's minimum of 100 cases on at least 60 distinct days is not reached (19 cases on 19 days).
- Reading: The profile is read from the recorded regime (the detector's components are not recorded and their 60- and 365-bar warm-ups lie outside the windows) and a down day from the raw one-day return < 0; the slope is a pooled OLS with intercept of the next-day excess return (fraction) on the forecast across all coins, with CR1 standard errors clustered by UTC day, and the cases are every bar with forecast > 0 (a 1-bar horizon makes every bar its own grid cell).
- Size: unusual move -0.05 % (t -0.10, the cases of one day together: 10 days) per case over 1 bars, -0.050 of the coin's usual move (6.78 %); normal drift in its direction +0.93 %, total +0.87 %; 10 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-01_agitated-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2016_2017/backtests/038-01_agitated-fall-next-day-rebound_1d`
Measure: `measure.py`
