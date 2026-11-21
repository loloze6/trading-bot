---
plan: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-day return minus normal drift on forecast, pooled non-overlapping grid cases: 0.00136849; OLS slope t: 2.4973 (threshold: confirm if slope t >= 2 with supporting check passing; reject if t <= -2; otherwise inconclusive)
- Supporting check: mean 10-day return minus normal drift among grid cases with forecast > 0, above 0: 0.00636288, passed: True
- Counts: grid cases: 1691, grid cases with forecast > 0: 837
- Decided by: The slope's t is 2 or more (2.50) and the supporting check passes.
- Reading: Situation = raw 28-day return > 0 with a long (positive) forecast, raw value recomputed from closes where missing; grid = rows 0,10,20,... of each window with close[t+10] in the same window; normal drift = each coin's mean grid 10-day return over all its windows; slope t from pooled OLS with intercept; the plan's 'fewer than 100 grid cases with forecast > 0' minimum is reported as 'not observable' per the workflow rule.
- Size: unusual move +0.75 % per case over 10 bars, 0.042 of the coin's usual move (14.49 %); normal drift in its direction +1.16 %, total +1.91 %; 882 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d`
Measure: `measure.py`
