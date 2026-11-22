---
plan: 025-02_deeper-fall-bigger-giveback_1d
idea: 025-02_deeper-fall-bigger-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of drift-adjusted 5-bar forward return on the case's forecast, pooled over coins: 0.864461; OLS slope t: 0.864461 (threshold: confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2; at least 30 cases)
- Supporting check: mean unusual 5-bar move in the short direction: -0.00251839, passed: False
- Counts: cases: 186
- Decided by: Inconclusive: the slope's t is between -2 and 2.
- Reading: Situation bars are recomputed from prices (90-bar return from the recorded fall_depth raw value where present, 1-bar return over the rolling 20-bar std of daily returns including the bar), falling back to the recorded regime 'mean_reversion' where the window lacks the history; a case is the first short bet (forecast fall of >= 2 points from its least negative level since the last bet, from 0 after a flat) in each 5-bar grid cell of a window with a full 5-bar forward return in that window; the minimum of 30 cases is treated as a minimum count (not observable).
- Size: unusual move -0.25 % per case over 5 bars, -0.023 of the coin's usual move (10.60 %); normal drift in its direction -0.61 %, total -0.86 %; 186 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback_1d`
Measure: `measure.py`
