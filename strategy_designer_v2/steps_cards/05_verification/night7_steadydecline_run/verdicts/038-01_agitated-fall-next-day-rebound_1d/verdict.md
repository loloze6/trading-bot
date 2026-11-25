---
plan: 038-01_agitated-fall-next-day-rebound_1d
idea: 038-01_agitated-fall-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (return per forecast point): 0.0010705; t clustered by day: 2.76736 (threshold: confirm: slope > 0 with t >= 2 and weighted mean > 0; reject: slope < 0 with t <= -2; min 100 cases on 60 distinct days)
- Supporting check: forecast-weighted mean next-day excess return above 0: 0.0120689, passed: True
- Counts: cases: 1468, distinct days: 702
- Decided by: The slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0.
- Reading: The profile is read from the recorded regime (the detector's components are not recorded and their 60- and 365-bar warm-ups lie outside the windows) and a down day from the raw one-day return < 0; the slope is a pooled OLS with intercept of the next-day excess return (fraction) on the forecast across all coins, with CR1 standard errors clustered by UTC day, and the cases are every bar with forecast > 0 (a 1-bar horizon makes every bar its own grid cell).
- Size: unusual move +0.99 % (t 3.38, the cases of one day together: 494 days) per case over 1 bars, 0.212 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.12 %; 999 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0006748 on the check folds against +0.001071 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-01_agitated-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/038-01_agitated-fall-next-day-rebound_1d`
Measure: `measure.py`
