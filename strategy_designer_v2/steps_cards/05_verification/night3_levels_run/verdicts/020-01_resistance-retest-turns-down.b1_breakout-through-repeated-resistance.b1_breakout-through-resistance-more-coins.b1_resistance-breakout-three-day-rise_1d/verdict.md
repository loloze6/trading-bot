---
plan: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise_1d
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar return over cases (return minus coin's 3-bar drift), pooled: 0.00189623; t of the mean: 1.32955 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: OLS slope of excess 3-bar return on post_pipeline_value at case bar: 0.000343403, passed: True
- Counts: cases: 4748, active bars: 6651
- Decided by: The t of the mean excess 3-bar return lies between -2 and 2.
- Reading: Cases are long-side forecast rises of at least 2 points (from the lowest long level since the last bet, 0 after flat), the first per 3-bar grid cell of each window, dropped when the 3-bar return leaves the window; drift is the coin's mean non-overlapping 3-bar return over all its windows.
- Size: unusual move +0.19 % per case over 3 bars, 0.018 of the coin's usual move (9.20 %); normal drift in its direction +0.44 %, total +0.63 %; 4748 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise_1d`
Measure: `measure.py`
