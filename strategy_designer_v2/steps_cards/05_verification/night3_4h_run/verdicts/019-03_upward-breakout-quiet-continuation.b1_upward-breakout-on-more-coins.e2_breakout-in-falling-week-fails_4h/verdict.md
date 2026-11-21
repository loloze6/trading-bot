---
plan: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 18-bar short return per case: 0.00834224; t of the mean: 4.43916 (threshold: t >= 2 with at least 30 cases (and deeper half ahead) confirms; t <= -2 with at least 30 cases rejects)
- Supporting check: deeper-fall half minus shallower half, mean drift-adjusted short return: 0.00172646, passed: True
- Counts: cases: 1834
- Decided by: Confirm: t >= 2 with at least 30 cases and the deeper-fall half ahead of the shallower half.
- Reading: Situation computed from prices (close above max high of previous 12 bars in the window, 42-bar return < 0, using the recorded week_fall raw value where present); active bars whose situation cannot be computed inside the window (115) are left out of the agreement share; a case is the first short bet (forecast falling >= 2 points below its highest short level since the last bet, reset to 0 after flat or a side change) in each 18-bar grid cell counted from each window's first row, cases without 18 bars left in the window are dropped, and the median split puts |forecast| above the median in the deeper half and the rest in the shallower half.
- Size: unusual move +0.83 % per case over 18 bars, 0.084 of the coin's usual move (9.29 %); normal drift in its direction -0.52 %, total +0.31 %; 1834 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h`
Measure: `measure.py`
