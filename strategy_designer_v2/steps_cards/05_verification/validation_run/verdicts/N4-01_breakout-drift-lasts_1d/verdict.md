---
plan: N4-01_breakout-drift-lasts_1d
idea: N4-01_breakout-drift-lasts
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar excess return of grid bars with forecast > 0, pooled: 0.0233349; t of the mean: 1.07383 (threshold: confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: mean 10-bar excess of regime grid bars below the 20-bar high: 0.0258675, passed: True
- Counts: pooled independent cases: 64, supporting cases: 44
- Decided by: t lies strictly between -2 and 2, which the plan calls inconclusive.
- Reading: Situation recomputed from closes inside each window (close above its prior 20 closes, bars since <= 9), falling back on the recorded regime where history is too short; the coin's mean 10-bar return is the mean over all its non-overlapping grid returns in all windows; the supporting check takes all grid bars in the regime with bars since the high >= 1, whatever their forecast; the plan's 'fewer than 20 pooled independent cases' is applied as a minimum count (not observable).
- Size: unusual move +3.43 % per case over 10 bars, 0.207 of the coin's usual move (15.86 %); normal drift in its direction +0.26 %, total +3.69 %; 82 cases
Plan: `steps_cards/03_test_plan/plans/N4-01_breakout-drift-lasts_1d.md`
Record: `steps_cards/04_backtest/backtests/N4-01_breakout-drift-lasts_1d`
Measure: `measure.py`
