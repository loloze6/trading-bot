---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-bar excess return on forecast, trending grid bars: 0.000839493; OLS slope t: 1.4361 (threshold: slope t >= 2 confirms (with top-minus-bottom third > 0); t <= -2 rejects)
- Supporting check: mean excess 5-bar return, top third minus bottom third of forecasts: 0.00899552, passed: True
- Counts: trending-regime grid cases: 1685
- Decided by: The slope's t lies between -2 and 2.
- Reading: Trending cases are grid bars (positions 0,5,10,... of each window with a full 5-bar forward return) whose recorded regime is 'trending', thirds are equal-count groups of floor(n/3) cases by forecast rank, the drift is the coin's mean non-overlapping 5-bar return over all its windows, and on a window's first 20 bars the situation check uses the recorded regime since the 20-day return cannot be recomputed in-window.
- Size: unusual move +0.33 % per case over 5 bars, 0.028 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.92 %; 1994 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d`
Measure: `measure.py`
