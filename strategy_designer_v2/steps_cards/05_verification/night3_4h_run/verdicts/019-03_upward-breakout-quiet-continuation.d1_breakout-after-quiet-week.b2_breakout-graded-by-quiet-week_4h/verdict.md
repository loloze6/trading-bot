---
plan: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar unusual move of breakout bets: 0.00204012; t of the mean: 1.29483 (threshold: confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: t <= -2)
- Supporting check: high-half minus low-half quiet mean unusual move: 0.00347345, passed: True
- Counts: cases: 3109, high-half cases: 1554, low-half cases: 1554
- Decided by: Neither rule met: the main t is between -2 and 2, or it is positive with a supporting difference <= 0 whose Welch t is above -2.
- Reading: The breakout is rebuilt from prices as close[t] > max(high[t-12..t-1]) inside each window, and the first 12 bars of a window, where it cannot be computed, are left out of the agreement; a case is a holding-period bet (a rise of a positive forecast of at least 2 points from its lowest level since the last bet, from 0 after a flat) on a trending bar, the first such bet in each 18-bar grid cell counted from the window's first row, with no case where the 18-bar return leaves the window; the normal drift is the coin's mean 18-bar return on the grid of all its windows; the halves are the cases strictly above and strictly below the median of quiet's post_pipeline_value (ties at the median left out); the plan's 'fewer than 30 cases / 15 per half' is reported as not observable.
- Size: unusual move +0.20 % per case over 18 bars, 0.023 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.61 %; 3109 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h`
Measure: `measure.py`
