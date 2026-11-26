---
plan: 044-01_agitated-wide-range-fall-rebound_1d
idea: 044-01_agitated-wide-range-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (forecast > 0 bars): 7.73931e-05; t clustered by day: 0.14464 (threshold: confirm: slope > 0 with day-clustered t >= 2 (and weighted mean > 0); reject: slope < 0 with t <= -2)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.00113575, passed: True
- Counts: cases with forecast > 0: 406, distinct days: 178
- Decided by: Inconclusive: the slope's day-clustered t lies between -2 and 2.
- Reading: Agitated profile read as regime == 'unknown' (not vetoed to chop), a down day as the recorded raw component > 0 (close below previous close where not recorded); cases are forecast > 0 bars with a next close in the same window; the clustered t uses the standard CR1 small-sample correction G/(G-1)*(N-1)/(N-K); the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow.
- Size: unusual move -0.13 % (t -0.33, the cases of one day together: 124 days) per case over 1 bars, -0.005 of the coin's usual move (3.33 %); normal drift in its direction +0.06 %, total -0.07 %; 252 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/044-01_agitated-wide-range-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/044-01_agitated-wide-range-fall-rebound_1d`
Measure: `measure.py`
