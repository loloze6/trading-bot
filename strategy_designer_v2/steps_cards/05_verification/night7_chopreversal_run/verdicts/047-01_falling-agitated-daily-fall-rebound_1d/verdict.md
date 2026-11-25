---
plan: 047-01_falling-agitated-daily-fall-rebound_1d
idea: 047-01_falling-agitated-daily-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, bars with forecast > 0: 0.0010705; slope t, SE clustered by day: 2.76736 (threshold: slope t (clustered by day) >= 2 and weighted mean > 0 confirms; t <= -2 rejects; else inconclusive)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.0120689, passed: True
- Counts: down-day cases: 1468, distinct days: 702
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: Profile bars are read from the recorded regime (not 'chop'), the raw one-day return from last_history_value (else recomputed from closes); the clustered standard error uses the usual small-sample factor G/(G-1)*(N-1)/(N-K) with an intercept in the regression; the plan's minimum counts (100 cases, 50 distinct days) are applied as 'not observable' per the workflow.
- Size: unusual move +0.99 % (t 3.38, the cases of one day together: 494 days) per case over 1 bars, 0.212 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.12 %; 999 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0006748 on the check folds against +0.001071 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/047-01_falling-agitated-daily-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/047-01_falling-agitated-daily-fall-rebound_1d`
Measure: `measure.py`
