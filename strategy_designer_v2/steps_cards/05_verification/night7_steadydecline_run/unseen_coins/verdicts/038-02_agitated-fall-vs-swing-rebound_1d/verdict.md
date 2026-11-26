---
plan: 038-02_agitated-fall-vs-swing-rebound_1d
idea: 038-02_agitated-fall-vs-swing-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on forecast, bars with forecast > 0: 0.000477552; OLS slope t: 1.9782 (threshold: confirm: slope t >= 2 (with mean excess > 0 and >= 100 cases); reject: slope t <= -2 or mean excess t <= -2 (>= 100 cases))
- Supporting check: mean next-day excess return on forecast > 0 bars above 0: 0.00230916, passed: True
- Counts: cases with forecast > 0: 1404
- Decided by: Inconclusive: the slope's t is between -2 and 2. (mean excess t = 1.570)
- Reading: Profile read from the recorded regime ('unknown' = no veto, i.e. falling agitated) since the detector's components are not recorded; the fall is a raw scaled return below 0 and the expected side long; the regression pools all coins' bars with forecast > 0, each coin's mean daily return taken over all its windows, and the cases are those bars with a next bar in the same window.
- Size: unusual move +0.18 % (t 0.52, the cases of one day together: 328 days) per case over 1 bars, 0.037 of the coin's usual move (5.40 %); normal drift in its direction +0.15 %, total +0.33 %; 909 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-02_agitated-fall-vs-swing-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Measure: `measure.py`
