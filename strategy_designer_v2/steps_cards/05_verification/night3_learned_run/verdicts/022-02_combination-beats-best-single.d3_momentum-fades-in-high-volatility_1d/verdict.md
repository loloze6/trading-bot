---
plan: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (20-bar forward return minus coin's normal 20-bar drift), non-overlapping grid, coins pooled: 0.00658229; t of the mean: 0.568387 (threshold: confirm: mean > 0 with t >= 2.0 and timing gain > 0; reject: mean < 0 with t <= -2.0; at least 300 grid cases)
- Supporting check: book timing gain (mean daily book return minus gain from market's own rise): 0.000342092, passed: True
- Counts: grid cases pooled: 827
- Decided by: The main t lies between -2.0 and 2.0 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: Every grid bar with a 20-bar forward return inside its window counts as a case, including flat (forecast 0) bars, and the coin's normal 20-bar drift is the mean of its grid forward returns over all windows; the plan's 'fewer than 300 grid cases' is treated as a minimum count, so it gives 'not observable'.
- Size: unusual move -0.44 % per case over 20 bars, -0.043 of the coin's usual move (21.24 %); normal drift in its direction -0.16 %, total -0.61 %; 753 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d`
Measure: `measure.py`
