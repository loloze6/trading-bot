---
plan: 013-05_longer-stall-bigger-breakout_1d
idea: 013-05_longer-stall-bigger-breakout
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 30-bar forward return on stall post_pipeline_value: None (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; on at least 30 cases)
- Supporting check: none
- Counts: trending grid bars: 18
- Decided by: Only 18 trending grid bars, fewer than the plan's minimum of 30 cases.
- Reading: Situation taken as regime 'trending' plus an in-window price check, side long; the coin mean is over all its complete grid bars in all windows (trending or not); grid bars without a full 30-bar forward return inside the window or without a recorded stall value are left out; the slope's t is the ordinary OLS t pooled across coins.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-05_longer-stall-bigger-breakout_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-05_longer-stall-bigger-breakout_1d`
Measure: `measure.py`
