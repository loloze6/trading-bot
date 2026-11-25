---
plan: 036-01_swing-scaled-fall-next-day-rebound_1d
idea: 036-01_swing-scaled-fall-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast: 0.000281788; slope t, clustered by day: 2.15065 (threshold: t >= 2 confirms (with supporting mean > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean next-day excess return on forecast > 0 bars above 0: 0.0012612, passed: True
- Counts: bars with forecast above 0: 18271, distinct days: 2413, bars in slope: 36948, day clusters: 2898
- Decided by: The slope's t is 2 or more and the mean excess next-day return on forecast > 0 bars is above 0.
- Reading: Situation = raw fall_in_swings value below 0 (a down day; day-return sign if not recorded) with forecast > 0 (long); slope t is cluster-robust by UTC day (CR1, all coins' bars of a day as one cluster); the 300-bar and 200-day minimums count bars with forecast above 0 that have a next-day return inside their window; coin mean daily return is over all its windows' next-day returns.
- Size: unusual move +0.09 % (t 0.66, the cases of one day together: 1988 days) per case over 1 bars, 0.017 of the coin's usual move (5.31 %); normal drift in its direction +0.15 %, total +0.24 %; 12027 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +4.22e-05 on the check folds against +0.0002818 on every fold
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/036-01_swing-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/036-01_swing-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
