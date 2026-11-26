---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
fit: exact
status: inconclusive
---
Situation check: 95 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 48-bar directional excess return over the coin's normal drift: 0.00148732; t of the mean: 0.388595 (threshold: confirm: t of the mean >= +2 with top-minus-bottom half above 0; reject: t <= -2; at least 100 cases)
- Supporting check: top half minus bottom half (median |forecast|) mean directional excess return: 0.00203789, passed: True
- Counts: cases: 532, top_half: 266, bottom_half: 266
- Decided by: The main mean's t lies between -2 and +2.
- Reading: Cases are all trending bars with nonzero forecast and a full 48-bar forward return in the same window, the drift is each coin's mean non-overlapping 48-bar return over all its windows, and the median split puts |forecast| > median in the top half and <= median in the bottom half.
- Size: unusual move +0.34 % (t 0.56, the cases of one day together: 199 days) per case over 48 bars, 0.024 of the coin's usual move (7.76 %); normal drift in its direction +0.14 %, total +0.47 %; 462 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_coins/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Measure: `measure.py`
