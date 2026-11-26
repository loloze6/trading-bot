---
plan: 047-01_falling-agitated-daily-fall-rebound_1d
idea: 047-01_falling-agitated-daily-fall-rebound
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, bars with forecast > 0: 0.00179144; slope t, SE clustered by day: 0.737809 (threshold: slope t (clustered by day) >= 2 and weighted mean > 0 confirms; t <= -2 rejects; else inconclusive)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.00554824, passed: True
- Counts: down-day cases: 19, distinct days: 19
- Decided by: Minimum count not reached: 19 down-day cases (need 100) on 19 distinct days (need 50).
- Reading: Profile bars are read from the recorded regime (not 'chop'), the raw one-day return from last_history_value (else recomputed from closes); the clustered standard error uses the usual small-sample factor G/(G-1)*(N-1)/(N-K) with an intercept in the regression; the plan's minimum counts (100 cases, 50 distinct days) are applied as 'not observable' per the workflow.
- Size: unusual move -0.05 % (t -0.10, the cases of one day together: 10 days) per case over 1 bars, -0.050 of the coin's usual move (6.78 %); normal drift in its direction +0.93 %, total +0.87 %; 10 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/047-01_falling-agitated-daily-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/047-01_falling-agitated-daily-fall-rebound_1d`
Measure: `measure.py`
