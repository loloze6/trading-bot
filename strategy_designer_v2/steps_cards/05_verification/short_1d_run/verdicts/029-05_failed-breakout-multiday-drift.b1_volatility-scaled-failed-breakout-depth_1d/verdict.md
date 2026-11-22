---
plan: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean 8-bar short-side excess fall: 0.020029; t of the weighted mean: 2.94072 (threshold: confirm: positive with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases)
- Supporting check: deeper-half minus shallower-half mean excess fall (split at median |forecast|): 0.0220325, passed: True
- Counts: cases: 389, deeper half: 194, shallower half: 195
- Decided by: The weighted mean short-side excess fall is positive with t >= 2 over at least 30 cases, and the deeper half's excess fall exceeds the shallower half's.
- Reading: Situation = non-zero raw fail_depth value (lag inside the component) with a short forecast; a case is the first short-side bet (forecast falling >= 2 points from its least-short level since the last bet, reset at flat) in each 8-bar grid cell from each window's first row, dropped if its 8-bar return leaves the window; drift is the coin's mean non-overlapping 8-bar return over all windows; the weighted mean's t uses the weighted (sandwich) standard error sqrt(sum w^2 (x-m)^2)/sum w; the halves are |forecast| above the median versus at or below it, compared by unweighted means.
- Size: unusual move +1.18 % per case over 8 bars, 0.084 of the coin's usual move (13.97 %); normal drift in its direction -1.06 %, total +0.12 %; 389 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d`
Measure: `measure.py`
