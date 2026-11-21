---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return over coin drift per case, before costs: 0.0192582; t of the mean: 2.04922 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean excess of breaks >= 1 range minus breaks < 1 range: 0.0330896, passed: True
- Counts: independent cases: 414, large-break cases: 115, small-break cases: 299
- Decided by: mean excess return above 0 with t >= 2 and large-minus-small break difference above 0
- Reading: situation = close above the prior-12-bar high (raw break > 0, or from prices where not recorded) and 42-bar close-to-close return > 0 inside the window, side long; active bars whose 42-bar return cannot be computed inside the window are left out of the agreement; a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet, reset after flat) in each 18-bar grid cell from the window's first row, with its 18-bar return inside the window minus the coin's mean non-overlapping 18-bar return over all windows, and the break size is the raw last_history_value on the signal bar
- Size: unusual move +1.93 % per case over 18 bars, 0.128 of the coin's usual move (13.56 %); normal drift in its direction +2.99 %, total +4.92 %; 414 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/unseen_2016_2017/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h`
Measure: `measure.py`
