---
plan: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: ordinary t of mean of post_pipeline_value x drift-adjusted 20-bar forward return, positive-forecast 20-bar grid bars: -0.034587; ordinary t of the mean: -0.136234 (threshold: confirm if t >= 2 with >= 30 cases and supporting check passes; reject if t <= -2 with >= 30 cases)
- Supporting check: upper-half minus lower-half (by forecast) mean drift-adjusted 20-bar return, positive-forecast grid bars: 0.0906845, passed: True
- Counts: positive-forecast grid cases: 41
- Decided by: The main-measure t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Grid = rows 0, 20, 40, ... of each window with a full 20-bar forward return inside the window; the coin's mean 20-bar return is the mean over all its grid bars of all windows; halves split by sorted forecast into the bottom and top n//2 cases (the middle case dropped when n is odd); fewer than 30 cases is reported as 'not observable'.
- Size: unusual move +4.96 % per case over 20 bars, 0.168 of the coin's usual move (21.24 %); normal drift in its direction +2.51 %, total +7.47 %; 152 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d`
Measure: `measure.py`
