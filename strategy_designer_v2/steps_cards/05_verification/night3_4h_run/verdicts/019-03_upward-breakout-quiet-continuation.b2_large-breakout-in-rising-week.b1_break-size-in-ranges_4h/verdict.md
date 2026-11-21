---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return over coin drift per case, before costs: 0.00434428; t of the mean: 2.302 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean excess of breaks >= 1 range minus breaks < 1 range: 0.0179705, passed: True
- Counts: independent cases: 2357, large-break cases: 509, small-break cases: 1848
- Decided by: mean excess return above 0 with t >= 2 and large-minus-small break difference above 0
- Reading: situation = close above the prior-12-bar high (raw break > 0, or from prices where not recorded) and 42-bar close-to-close return > 0 inside the window, side long; active bars whose 42-bar return cannot be computed inside the window are left out of the agreement; a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet, reset after flat) in each 18-bar grid cell from the window's first row, with its 18-bar return inside the window minus the coin's mean non-overlapping 18-bar return over all windows, and the break size is the raw last_history_value on the signal bar
- Size: unusual move +0.43 % per case over 18 bars, 0.048 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.84 %; 2357 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h`
Measure: `measure.py`
