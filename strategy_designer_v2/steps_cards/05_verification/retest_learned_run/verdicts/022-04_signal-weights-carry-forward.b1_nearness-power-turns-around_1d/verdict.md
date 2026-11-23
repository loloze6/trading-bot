---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (5-bar return minus coin's mean 5-bar return), non-overlapping, pooled: 0.00457219; t of the mean: 1.96751 (threshold: confirm: mean > 0 with t >= 2 over >= 300 cases and timing gain > 0; reject: mean < 0 with t <= -2 over >= 300 cases)
- Supporting check: book mean daily return before costs minus gain from market's rise: 0.000489747, passed: True
- Counts: non-overlapping cases: 3042, active bars: 15585
- Decided by: The t lies between -2 and 2.
- Reading: Every grid row (0, 5, 10, ...) with a 5-bar return inside its window is a case, flat forecasts included as zero products, and the coin's mean 5-bar return is taken over the same grid of all its windows.
- Size: unusual move +0.30 % per case over 5 bars, 0.039 of the coin's usual move (10.47 %); normal drift in its direction -0.00 %, total +0.29 %; 1466 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d`
Measure: `measure.py`
