---
plan: 038-02_agitated-fall-vs-swing-rebound_1d
idea: 038-02_agitated-fall-vs-swing-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on forecast, bars with forecast > 0: 0.0010552; OLS slope t: 4.79687 (threshold: confirm: slope t >= 2 (with mean excess > 0 and >= 100 cases); reject: slope t <= -2 or mean excess t <= -2 (>= 100 cases))
- Supporting check: mean next-day excess return on forecast > 0 bars above 0: 0.00703452, passed: True
- Counts: cases with forecast > 0: 1468
- Decided by: Confirm: the slope's t is 2 or more, the mean next-day excess return is above 0, with at least 100 cases. (mean excess t = 5.041)
- Reading: Profile read from the recorded regime ('unknown' = no veto, i.e. falling agitated) since the detector's components are not recorded; the fall is a raw scaled return below 0 and the expected side long; the regression pools all coins' bars with forecast > 0, each coin's mean daily return taken over all its windows, and the cases are those bars with a next bar in the same window.
- Size: unusual move +0.99 % (t 3.34, the cases of one day together: 478 days) per case over 1 bars, 0.212 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.12 %; 975 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0007151 on the check folds against +0.001055 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-02_agitated-fall-vs-swing-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Measure: `measure.py`
