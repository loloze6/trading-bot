---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
fit: exact
status: confirmed
---
Situation check: 93 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 48-bar directional excess return over the coin's normal drift: 0.0109812; t of the mean: 2.52967 (threshold: confirm: t of the mean >= +2 with top-minus-bottom half above 0; reject: t <= -2; at least 100 cases)
- Supporting check: top half minus bottom half (median |forecast|) mean directional excess return: 0.00166139, passed: True
- Counts: cases: 466, top_half: 233, bottom_half: 233
- Decided by: The main mean's t is +2 or more and the top half minus bottom half is above 0.
- Reading: Cases are all trending bars with nonzero forecast and a full 48-bar forward return in the same window, the drift is each coin's mean non-overlapping 48-bar return over all its windows, and the median split puts |forecast| > median in the top half and <= median in the bottom half.
- Size: unusual move +1.37 % per case over 48 bars, 0.193 of the coin's usual move (6.56 %); normal drift in its direction +0.07 %, total +1.43 %; 405 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Measure: `measure.py`
