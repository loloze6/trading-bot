---
plan: 072-02.b1.b1_choppy-deep-up-day-five-day-fade_1d
idea: 072-02.b1.b1_choppy-deep-up-day-five-day-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day return minus drift on forecast, pooled, day-clustered: 0.00113393; day-clustered slope t: 0.9368 (threshold: confirm if slope t >= 2 (with supporting check), reject if slope t <= -2, with at least 30 cases)
- Supporting check: mean unusual 5-day move in the short direction > 0: 0.000244515, passed: True
- Counts: cases: 841, days: 295
- Decided by: Slope t lies between -2 and 2 with at least 30 cases.
- Reading: Up day recomputed from consecutive closes inside each window (the detector's regime on a window's first bar), situation = up day with the recorded depth at or below 0, side short; grid = rows 0,5,10,... of each window with a 5-bar return inside it; drift = coin's mean grid 5-day return over all its windows; OLS with intercept, CR1 cluster-robust SE by UTC day; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.78 % (t 2.18, the cases of one day together: 936 days) per case over 5 bars, 0.068 of the coin's usual move (12.35 %); normal drift in its direction -0.80 %, total -0.03 %; 1888 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-02.b1.b1_choppy-deep-up-day-five-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-02.b1.b1_choppy-deep-up-day-five-day-fade_1d`
Measure: `measure.py`
