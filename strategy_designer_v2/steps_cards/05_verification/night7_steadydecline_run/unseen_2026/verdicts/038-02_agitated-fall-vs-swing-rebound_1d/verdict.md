---
plan: 038-02_agitated-fall-vs-swing-rebound_1d
idea: 038-02_agitated-fall-vs-swing-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on forecast, bars with forecast > 0: 1.516e-05; OLS slope t: 0.0277478 (threshold: confirm: slope t >= 2 (with mean excess > 0 and >= 100 cases); reject: slope t <= -2 or mean excess t <= -2 (>= 100 cases))
- Supporting check: mean next-day excess return on forecast > 0 bars above 0: -2.16871e-05, passed: False
- Counts: cases with forecast > 0: 216
- Decided by: Inconclusive: the slope's t is between -2 and 2. (mean excess t = -0.007)
- Reading: Profile read from the recorded regime ('unknown' = no veto, i.e. falling agitated) since the detector's components are not recorded; the fall is a raw scaled return below 0 and the expected side long; the regression pools all coins' bars with forecast > 0, each coin's mean daily return taken over all its windows, and the cases are those bars with a next bar in the same window.
- Size: unusual move +0.03 % (t 0.04, the cases of one day together: 60 days) per case over 1 bars, 0.025 of the coin's usual move (3.33 %); normal drift in its direction +0.04 %, total +0.07 %; 130 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-02_agitated-fall-vs-swing-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2026/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Measure: `measure.py`
