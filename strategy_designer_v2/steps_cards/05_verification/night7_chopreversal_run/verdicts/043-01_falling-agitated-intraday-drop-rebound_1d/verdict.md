---
plan: 043-01_falling-agitated-intraday-drop-rebound_1d
idea: 043-01_falling-agitated-intraday-drop-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (day-clustered t): 0.000924804; day-clustered t of the slope: 3.04012 (threshold: confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2)
- Supporting check: forecast-weighted mean excess return of cases > 0: 0.0102893, passed: True
- Counts: cases: 1467, distinct days: 698
- Decided by: The slope has a t of 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: Profile bars are those with regime 'unknown' (not vetoed to chop); the drop is the recorded raw oc_drop value, recomputed from open/close where missing; the coin's mean daily return is the mean of all its within-window 1-bar returns; cluster-robust SE uses the usual G/(G-1)*(N-1)/(N-K) correction; days are UTC dates of the bar; the plan's minimum counts give 'not observable' when unmet.
- Size: unusual move +0.96 % (t 3.30, the cases of one day together: 511 days) per case over 1 bars, 0.206 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.09 %; 1037 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005854 on the check folds against +0.0009248 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/043-01_falling-agitated-intraday-drop-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/043-01_falling-agitated-intraday-drop-rebound_1d`
Measure: `measure.py`
