---
plan: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean 8-bar short-side excess fall: 0.00513127; t of the weighted mean: 0.211639 (threshold: confirm: positive with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases)
- Supporting check: deeper-half minus shallower-half mean excess fall (split at median |forecast|): 0.0131744, passed: True
- Counts: cases: 45, deeper half: 22, shallower half: 23
- Decided by: The t of the weighted mean short-side excess fall lies between -2 and 2.
- Reading: Situation = non-zero raw fail_depth value (lag inside the component) with a short forecast; a case is the first short-side bet (forecast falling >= 2 points from its least-short level since the last bet, reset at flat) in each 8-bar grid cell from each window's first row, dropped if its 8-bar return leaves the window; drift is the coin's mean non-overlapping 8-bar return over all windows; the weighted mean's t uses the weighted (sandwich) standard error sqrt(sum w^2 (x-m)^2)/sum w; the halves are |forecast| above the median versus at or below it, compared by unweighted means.
- Size: unusual move +0.17 % (t 0.08, the cases of one day together: 35 days) per case over 8 bars, -0.056 of the coin's usual move (9.38 %); normal drift in its direction -0.46 %, total -0.29 %; 45 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/unseen_2026/backtests/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d`
Measure: `measure.py`
