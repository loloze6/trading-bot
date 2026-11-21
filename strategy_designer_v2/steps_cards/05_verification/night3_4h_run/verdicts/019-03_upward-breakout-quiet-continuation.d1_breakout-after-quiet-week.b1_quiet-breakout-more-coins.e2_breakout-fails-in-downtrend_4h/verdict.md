---
plan: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 72-bar move per case: 0.0254624; t of the mean: 5.26007 (threshold: confirm: mean > 0 with t >= 2 (and correlation > 0); reject: mean < 0 with t <= -2)
- Supporting check: Pearson correlation of |forecast| at signal bar with short-direction unusual move: 0.0128737, passed: True
- Counts: cases across all coins and windows: 1375
- Decided by: Mean short-direction unusual move above 0 with t >= 2 and a positive correlation between |forecast| and the move.
- Reading: A case is the first short-side bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, reset to 0 when flat) in each 72-bar grid cell counted from the window's first row, kept only if 72 bars remain in the window; the drift is the mean non-overlapping 72-bar return over all the coin's windows; the correlation is Pearson; breakout for the situation check is close above the max high of the 12 preceding bars.
- Size: unusual move +2.55 % per case over 72 bars, 0.127 of the coin's usual move (19.52 %); normal drift in its direction -2.21 %, total +0.34 %; 1375 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h`
Measure: `measure.py`
