---
plan: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
idea: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 24-bar move per case, pooled, in the signal's direction: 0.000785267; ordinary t of the mean: 2.06563 (threshold: confirm t >= 2 over >= 30 cases (with top-quartile difference > 0); reject t <= -2 over >= 30 cases)
- Supporting check: mean unusual move of top-quartile |forecast| cases minus that of other cases: 0.0010879, passed: True
- Counts: cases: 17242, top_quartile_cases: 4311, other_cases: 12931
- Decided by: The main measure has t >= 2 over at least 30 cases and the top-quartile difference is above 0.
- Reading: A case is the first bet (a rise of |forecast| of >= 2 points on its side from its lowest level since the last bet, reset at flat or side change) in each 24-bar grid cell counted from each window's first row, the drift is the mean of the coin's 24-bar returns on that grid over all its windows, and the top quartile is the cases with |forecast| at or above the 75th percentile of the cases' |forecast|.
- Size: unusual move +0.08 % per case over 24 bars, 0.016 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.08 %; 17242 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h`
Measure: `measure.py`
