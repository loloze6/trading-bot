---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar forward return minus coin drift on forecast, trending grid bars: -0.000299125; OLS t of the slope: -1.15171 (threshold: t >= 2 with at least 200 cases to confirm; t <= -2 with at least 200 cases to reject)
- Supporting check: book mean daily return minus gain from market rise (timing part) > 0: -0.000529466, passed: False
- Counts: non-overlapping trending cases: 1662
- Decided by: The slope's t is between -2 and 2 with at least 200 cases.
- Reading: The regression pools all coins' grid bars (positions 0,5,10,... of each window with a full 5-bar return inside it) that are trending with non-zero forecast, the drift is each coin's mean 5-bar return on that grid over all its windows, and the book's daily return is the change of postRebalance_total_value between consecutive daily bars with the market gain taken as the previous bar's held allocation times the coin's mean daily return.
- Size: unusual move -0.65 % per case over 5 bars, -0.058 of the coin's usual move (10.60 %); normal drift in its direction -0.09 %, total -0.74 %; 1643 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d`
Measure: `measure.py`
