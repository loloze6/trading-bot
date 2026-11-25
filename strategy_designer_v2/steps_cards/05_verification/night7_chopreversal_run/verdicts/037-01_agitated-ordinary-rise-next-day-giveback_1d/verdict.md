---
plan: 037-01_agitated-ordinary-rise-next-day-giveback_1d
idea: 037-01_agitated-ordinary-rise-next-day-giveback
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return over drift, short direction: 0.00384875; t, cases of one day taken together: 2.19879 (threshold: confirm: mean > 0 with t >= 2 and slope < 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess return on raw scaled rise: -0.00226107, passed: True
- Counts: cases: 1865, distinct days: 1014
- Decided by: The main mean is positive with t >= 2 and the supporting slope is below 0 (confirm rule).
- Reading: Agitation is read from the recorded regime (not 'chop', the profile veto) since the 365-day volatility percentile cannot be rebuilt inside a window, the scaled rise from last_history_value or else from window prices; cases are the short-side bets of the forecast (rise of at least 2 points from its lowest level since the last bet) on every bar with a next-day close in the same window; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the slope is the OLS of the unflipped excess return on the raw rise; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow.
- Size: unusual move +0.38 % (t 2.20, the cases of one day together: 1014 days) per case over 1 bars, 0.082 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.26 %; 1865 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0004633 on the check folds against +0.003849 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/037-01_agitated-ordinary-rise-next-day-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/037-01_agitated-ordinary-rise-next-day-giveback_1d`
Measure: `measure.py`
