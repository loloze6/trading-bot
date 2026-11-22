---
plan: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
fit: exact
status: inconclusive
---
Situation check: 95 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 48-bar forward return minus normal drift regressed on forecast, pooled: 0.000103974; OLS slope t: 0.863673 (threshold: confirm if t >= 2 (with positive mean unusual move); reject if t <= -2)
- Supporting check: mean unusual move in forecast's direction > 0: -0.000773637, passed: False
- Counts: cases over all coins: 1948, case bars before forward-return filter: 1985
- Decided by: The slope's t is between -2 and 2.
- Reading: Cases are Sunday 23:00 UTC bars (bar start) in regime mean_reversion with nonzero forecast and a full 48-bar forward return inside the window, the regressed variable is the undirected unusual return (OLS with intercept), and the plan's 'fewer than 200 cases' minimum is applied as 'not observable' per the workflow's rule on minimum counts.
- Size: unusual move -0.00 % per case over 48 bars, 0.002 of the coin's usual move (6.56 %); normal drift in its direction -0.01 %, total -0.01 %; 1741 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h`
Measure: `measure.py`
