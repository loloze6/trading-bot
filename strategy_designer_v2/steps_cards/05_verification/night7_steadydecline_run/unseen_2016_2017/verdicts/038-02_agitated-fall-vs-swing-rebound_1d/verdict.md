---
plan: 038-02_agitated-fall-vs-swing-rebound_1d
idea: 038-02_agitated-fall-vs-swing-rebound
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on forecast, bars with forecast > 0: 0.000600588; OLS slope t: 0.255496 (threshold: confirm: slope t >= 2 (with mean excess > 0 and >= 100 cases); reject: slope t <= -2 or mean excess t <= -2 (>= 100 cases))
- Supporting check: mean next-day excess return on forecast > 0 bars above 0: 0.00147315, passed: True
- Counts: cases with forecast > 0: 19
- Decided by: Fewer than 100 cases with forecast > 0: the plan's minimum count is not reached. (mean excess t = 0.179)
- Reading: Profile read from the recorded regime ('unknown' = no veto, i.e. falling agitated) since the detector's components are not recorded; the fall is a raw scaled return below 0 and the expected side long; the regression pools all coins' bars with forecast > 0, each coin's mean daily return taken over all its windows, and the cases are those bars with a next bar in the same window.
- Size: unusual move +0.00 % (t 0.01, the cases of one day together: 12 days) per case over 1 bars, -0.030 of the coin's usual move (6.78 %); normal drift in its direction +0.86 %, total +0.87 %; 12 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-02_agitated-fall-vs-swing-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2016_2017/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Measure: `measure.py`
