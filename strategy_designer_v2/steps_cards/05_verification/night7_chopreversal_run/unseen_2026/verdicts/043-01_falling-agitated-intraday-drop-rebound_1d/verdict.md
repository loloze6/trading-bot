---
plan: 043-01_falling-agitated-intraday-drop-rebound_1d
idea: 043-01_falling-agitated-intraday-drop-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (day-clustered t): -0.000334037; day-clustered t of the slope: -0.395956 (threshold: confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2)
- Supporting check: forecast-weighted mean excess return of cases > 0: -0.00136791, passed: False
- Counts: cases: 217, distinct days: 91
- Decided by: The slope t is between -2 and 2.
- Reading: Profile bars are those with regime 'unknown' (not vetoed to chop); the drop is the recorded raw oc_drop value, recomputed from open/close where missing; the coin's mean daily return is the mean of all its within-window 1-bar returns; cluster-robust SE uses the usual G/(G-1)*(N-1)/(N-K) correction; days are UTC dates of the bar; the plan's minimum counts give 'not observable' when unmet.
- Size: unusual move -0.14 % (t -0.23, the cases of one day together: 64 days) per case over 1 bars, -0.023 of the coin's usual move (3.33 %); normal drift in its direction +0.04 %, total -0.10 %; 134 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/043-01_falling-agitated-intraday-drop-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/043-01_falling-agitated-intraday-drop-rebound_1d`
Measure: `measure.py`
