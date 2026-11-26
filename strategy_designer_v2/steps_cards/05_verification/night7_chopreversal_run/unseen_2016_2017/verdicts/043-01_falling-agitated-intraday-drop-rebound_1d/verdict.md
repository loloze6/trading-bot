---
plan: 043-01_falling-agitated-intraday-drop-rebound_1d
idea: 043-01_falling-agitated-intraday-drop-rebound
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (day-clustered t): 0.00124819; day-clustered t of the slope: 1.01988 (threshold: confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2)
- Supporting check: forecast-weighted mean excess return of cases > 0: 0.00539128, passed: True
- Counts: cases: 20, distinct days: 20
- Decided by: The plan's minimum counts are not reached (20 cases, need 100; 20 distinct days, need 50).
- Reading: Profile bars are those with regime 'unknown' (not vetoed to chop); the drop is the recorded raw oc_drop value, recomputed from open/close where missing; the coin's mean daily return is the mean of all its within-window 1-bar returns; cluster-robust SE uses the usual G/(G-1)*(N-1)/(N-K) correction; days are UTC dates of the bar; the plan's minimum counts give 'not observable' when unmet.
- Size: unusual move +1.05 % (t 1.08, the cases of one day together: 13 days) per case over 1 bars, 0.133 of the coin's usual move (6.78 %); normal drift in its direction +0.91 %, total +1.96 %; 13 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/043-01_falling-agitated-intraday-drop-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/043-01_falling-agitated-intraday-drop-rebound_1d`
Measure: `measure.py`
