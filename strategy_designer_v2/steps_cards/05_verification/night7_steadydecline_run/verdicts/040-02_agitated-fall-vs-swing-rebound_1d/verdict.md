---
plan: 040-02_agitated-fall-vs-swing-rebound_1d
idea: 040-02_agitated-fall-vs-swing-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast, profile bars: 0.000636229; slope t, day-clustered: 3.17556 (threshold: slope t >= 2 confirms (with supporting check), <= -2 rejects)
- Supporting check: mean excess next-day return, forecast > 0: 0.00376862, passed: True
- Counts: profile bars with forecast above 0: 3753, distinct days: 1449, profile bars used: 7715
- Decided by: The slope's t is 2 or more and the mean excess next-day return over forecast>0 bars is above 0.
- Reading: Profile bars are those where the strategy's regime was active (component recorded, regime not 'chop'); the coin's mean is the mean 1-day return over all its windows; the slope t uses day-clustered standard errors (CR1 correction); minimum counts are taken over profile bars with forecast above 0 and a next-day return inside the window.
- Size: unusual move +0.34 % (t 1.67, the cases of one day together: 1050 days) per case over 1 bars, 0.076 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.47 %; 2469 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003207 on the check folds against +0.0006362 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/040-02_agitated-fall-vs-swing-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/040-02_agitated-fall-vs-swing-rebound_1d`
Measure: `measure.py`
