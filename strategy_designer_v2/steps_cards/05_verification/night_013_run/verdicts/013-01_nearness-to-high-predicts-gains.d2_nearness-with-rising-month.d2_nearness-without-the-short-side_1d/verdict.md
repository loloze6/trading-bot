---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 7-bar forward return minus coin's grid mean, forecast > 0 grid bars, pooled: 0.00690425; t of the mean: 1.71472 (threshold: confirm if t >= 2 and supporting check passes; reject if t <= -2)
- Supporting check: upper-half minus lower-half mean excess return (median forecast split): 0.0185327, passed: True
- Counts: independent forecast > 0 cases: 1199, upper half cases: 599, lower half cases: 600
- Decided by: The main measure's t is between -2 and 2.
- Reading: Grid bars are positions 0, 7, 14, ... of each window with a 7-bar forward return inside the window; the coin mean is over all such grid bars of all windows; the median split puts forecast > median in the upper half and forecast <= median in the lower half; the 100-case minimum is applied as 'not observable'.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d`
Measure: `measure.py`
