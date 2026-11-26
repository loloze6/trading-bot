---
plan: 047-01_falling-agitated-daily-fall-rebound_1d
idea: 047-01_falling-agitated-daily-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, bars with forecast > 0: 0.000452843; slope t, SE clustered by day: 1.00924 (threshold: slope t (clustered by day) >= 2 and weighted mean > 0 confirms; t <= -2 rejects; else inconclusive)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.00425021, passed: True
- Counts: down-day cases: 1404, distinct days: 444
- Decided by: The slope's t is between -2 and 2.
- Reading: Profile bars are read from the recorded regime (not 'chop'), the raw one-day return from last_history_value (else recomputed from closes); the clustered standard error uses the usual small-sample factor G/(G-1)*(N-1)/(N-K) with an intercept in the regression; the plan's minimum counts (100 cases, 50 distinct days) are applied as 'not observable' per the workflow.
- Size: unusual move +0.18 % (t 0.52, the cases of one day together: 330 days) per case over 1 bars, 0.037 of the coin's usual move (5.40 %); normal drift in its direction +0.14 %, total +0.33 %; 912 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/047-01_falling-agitated-daily-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_coins/backtests/047-01_falling-agitated-daily-fall-rebound_1d`
Measure: `measure.py`
