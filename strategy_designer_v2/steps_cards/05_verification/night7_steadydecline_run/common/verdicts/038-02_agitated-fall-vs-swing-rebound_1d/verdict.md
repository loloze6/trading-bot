---
plan: 038-02_agitated-fall-vs-swing-rebound_1d
idea: 038-02_agitated-fall-vs-swing-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on forecast, bars with forecast > 0: 0.000657505; OLS slope t: 4.9747 (threshold: confirm: slope t >= 2 (with mean excess > 0 and >= 100 cases); reject: slope t <= -2 or mean excess t <= -2 (>= 100 cases))
- Supporting check: mean next-day excess return on forecast > 0 bars above 0: 0.00275159, passed: True
- Counts: cases with forecast > 0: 4200
- Decided by: Confirm: the slope's t is 2 or more, the mean next-day excess return is above 0, with at least 100 cases. (mean excess t = 3.412)
- Reading: Profile read from the recorded regime ('unknown' = no veto, i.e. falling agitated) since the detector's components are not recorded; the fall is a raw scaled return below 0 and the expected side long; the regression pools all coins' bars with forecast > 0, each coin's mean daily return taken over all its windows, and the cases are those bars with a next bar in the same window.
- Size: unusual move +0.37 % (t 1.43, the cases of one day together: 736 days) per case over 1 bars, 0.072 of the coin's usual move (5.12 %); normal drift in its direction +0.11 %, total +0.48 %; 2677 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/038-02_agitated-fall-vs-swing-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/common/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Measure: `measure.py`
