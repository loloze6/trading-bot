---
plan: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d
idea: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 26-bar move after the cross (return minus coin's normal drift): 0.0582771; ordinary t of the mean: 0.688599 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: larger-forecast half minus smaller-forecast half, mean unusual move: -0.0791198, passed: False
- Counts: independent cases: 11
- Decided by: Only 11 independent cases, fewer than the plan's minimum of 20 over all coins and windows.
- Reading: Cloud recomputed in-window from prices (9/26/52, displaced 26); active bars whose cloud history is not inside the window are left out of the agreement, which also requires a long forecast and a negative raw 26-bar return; cases are bars with forecast >= 2, first one per 26-bar grid cell from each window's first row with 26 bars left; normal drift is the coin's mean non-overlapping 26-bar return over all its windows; the median split puts cases above the median forecast in the larger half and the rest in the smaller half; the plan's 'fewer than 20 independent cases' is applied as the minimum count (not observable).
- Size: unusual move +5.83 % per case over 26 bars, 0.327 of the coin's usual move (25.48 %); normal drift in its direction +3.94 %, total +9.77 %; 11 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d`
Measure: `measure.py`
