---
plan: 040-01_agitated-daily-fall-next-day-rebound_1d
idea: 040-01_agitated-daily-fall-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of (next-day return minus coin mean daily return) on forecast, bars with forecast > 0: 0.00052954; OLS slope t, day-clustered standard errors: 2.18444 (threshold: slope t >= 2 (with supporting mean > 0) confirms; slope t <= -2 rejects)
- Supporting check: mean next-day return minus coin mean daily return on bars with forecast > 0: 0.00376862, passed: True
- Counts: bars with forecast > 0 across all coins and windows: 3753, days: 1449
- Decided by: The slope's t is 2 or more and the supporting mean is above 0 (confirm rule).
- Reading: The regression has an intercept and its slope t uses cluster-robust (sandwich) standard errors with cases grouped by UTC day and the usual G/(G-1)*(N-1)/(N-K) correction; the coin's mean daily return is the mean of all its 1-bar returns over all its windows, and the 1-bar horizon makes every bar its own non-overlapping case.
- Size: unusual move +0.33 % (t 1.66, the cases of one day together: 1083 days) per case over 1 bars, 0.074 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.46 %; 2553 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003694 on the check folds against +0.0005295 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/040-01_agitated-daily-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/040-01_agitated-daily-fall-next-day-rebound_1d`
Measure: `measure.py`
