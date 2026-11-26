---
plan: 038-01_agitated-fall-next-day-rebound_1d
idea: 038-01_agitated-fall-next-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (return per forecast point): 0.000452843; t clustered by day: 1.00924 (threshold: confirm: slope > 0 with t >= 2 and weighted mean > 0; reject: slope < 0 with t <= -2; min 100 cases on 60 distinct days)
- Supporting check: forecast-weighted mean next-day excess return above 0: 0.00425021, passed: True
- Counts: cases: 1404, distinct days: 444
- Decided by: The slope's t lies between -2 and 2.
- Reading: The profile is read from the recorded regime (the detector's components are not recorded and their 60- and 365-bar warm-ups lie outside the windows) and a down day from the raw one-day return < 0; the slope is a pooled OLS with intercept of the next-day excess return (fraction) on the forecast across all coins, with CR1 standard errors clustered by UTC day, and the cases are every bar with forecast > 0 (a 1-bar horizon makes every bar its own grid cell).
- Size: unusual move +0.18 % (t 0.52, the cases of one day together: 330 days) per case over 1 bars, 0.037 of the coin's usual move (5.40 %); normal drift in its direction +0.14 %, total +0.33 %; 912 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-01_agitated-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/038-01_agitated-fall-next-day-rebound_1d`
Measure: `measure.py`
