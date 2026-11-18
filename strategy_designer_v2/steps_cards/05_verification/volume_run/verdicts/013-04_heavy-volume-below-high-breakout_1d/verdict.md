---
plan: 013-04_heavy-volume-below-high-breakout_1d
idea: 013-04_heavy-volume-below-high-breakout
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 30-bar excess return on vol_ratio post_pipeline_value at break bars: 0.0358023; OLS slope t: 2.46463 (threshold: confirm: slope > 0 with t >= 2 on >= 20 cases; reject: slope < 0 with t <= -2 on >= 20 cases)
- Supporting check: none
- Counts: cases: 49
- Decided by: The slope is positive with t = 2.46 >= 2 on 49 cases (>= 20): the confirm rule.
- Reading: The situation is checked as a necessary condition, close above the highest high of the prior bars available inside the window (at most 365, the window's first bar counted as consistent) with a positive forecast, since the 365-bar history is not recorded; a break bar is a 'trending' regime bar whose previous row in the same window is not 'trending' (a window's first row is not a case), and the coin's mean 30-bar return is taken on the non-overlapping grid (positions 0, 30, 60, ...) of all its windows pooled.
Plan: `steps_cards/03_test_plan/volume_run/plans/013-04_heavy-volume-below-high-breakout_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-04_heavy-volume-below-high-breakout_1d`
Measure: `measure.py`
