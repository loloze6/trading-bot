---
plan: 044-01_agitated-wide-range-fall-rebound_1d
idea: 044-01_agitated-wide-range-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (forecast > 0 bars): 0.00044874; t clustered by day: 2.45332 (threshold: confirm: slope > 0 with day-clustered t >= 2 (and weighted mean > 0); reject: slope < 0 with t <= -2)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.00484982, passed: True
- Counts: cases with forecast > 0: 10012, distinct days: 2226
- Decided by: Confirm: the slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0.
- Reading: Agitated profile read as regime == 'unknown' (not vetoed to chop), a down day as the recorded raw component > 0 (close below previous close where not recorded); cases are forecast > 0 bars with a next close in the same window; the clustered t uses the standard CR1 small-sample correction G/(G-1)*(N-1)/(N-K); the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow.
- Size: unusual move +0.17 % (t 0.94, the cases of one day together: 1610 days) per case over 1 bars, 0.034 of the coin's usual move (5.12 %); normal drift in its direction +0.12 %, total +0.29 %; 6110 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/044-01_agitated-wide-range-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/common/backtests/044-01_agitated-wide-range-fall-rebound_1d`
Measure: `measure.py`
