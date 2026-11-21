---
plan: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-day return minus normal drift on forecast, pooled non-overlapping grid cases: 0.00446745; OLS slope t: 2.0693 (threshold: confirm if slope t >= 2 with supporting check passing; reject if t <= -2; otherwise inconclusive)
- Supporting check: mean 10-day return minus normal drift among grid cases with forecast > 0, above 0: 0.0229263, passed: True
- Counts: grid cases: 284, grid cases with forecast > 0: 183
- Decided by: The slope's t is 2 or more (2.07) and the supporting check passes.
- Reading: Situation = raw 28-day return > 0 with a long (positive) forecast, raw value recomputed from closes where missing; grid = rows 0,10,20,... of each window with close[t+10] in the same window; normal drift = each coin's mean grid 10-day return over all its windows; slope t from pooled OLS with intercept; the plan's 'fewer than 100 grid cases with forecast > 0' minimum is reported as 'not observable' per the workflow rule.
- Size: unusual move +5.92 % per case over 10 bars, 0.209 of the coin's usual move (30.80 %); normal drift in its direction +9.90 %, total +15.82 %; 178 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d`
Measure: `measure.py`
