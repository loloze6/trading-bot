---
plan: 013-04_heavy-volume-below-high-breakout_1d
idea: 013-04_heavy-volume-below-high-breakout
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 30-bar excess return on vol_ratio post_pipeline_value at break bars: 0.0278198; OLS slope t: 1.61512 (threshold: confirm: slope > 0 with t >= 2 on >= 20 cases; reject: slope < 0 with t <= -2 on >= 20 cases)
- Supporting check: none
- Counts: cases: 34
- Decided by: t = 1.62 lies between -2 and 2 on 34 cases: the inconclusive rule.
- Reading: The situation is checked as a necessary condition, close above the highest high of the prior bars available inside the window (at most 365, the window's first bar counted as consistent) with a positive forecast, since the 365-bar history is not recorded; a break bar is a 'trending' regime bar whose previous row in the same window is not 'trending' (a window's first row is not a case), and the coin's mean 30-bar return is taken on the non-overlapping grid (positions 0, 30, 60, ...) of all its windows pooled.
- Size: unusual move +19.90 % (t 2.41, the cases of one day together: 34 days) per case over 30 bars, 0.522 of the coin's usual move (34.93 %); normal drift in its direction +6.79 %, total +26.70 %; 42 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/013-04_heavy-volume-below-high-breakout_1d.md`
Record: `steps_cards/04_backtest/volume_run/unseen_coins/backtests/013-04_heavy-volume-below-high-breakout_1d`
Measure: `measure.py`
