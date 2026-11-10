---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: excess forward 20-bar return while short (vs all-bar window mean), non-overlapping blocks: 0.0102576; t of the mean excess across short blocks: 0.318951 (threshold: confirm if excess < 0 with t <= -2 and slope not positive; reject if excess > 0 with t >= +2; otherwise inconclusive; inconclusive if fewer than 6 short blocks (120 short bars))
- Supporting check: slope of forward 20-bar return on |forecast| within short bars (should be <= 0); share of short blocks with negative excess: -0.00459134, passed: True
- Counts: short_blocks: 20, short_bars: 437
- Decided by: Inconclusive: t lies between -2 and +2.
- Reading: Each short block's excess is its forward 20-bar return (grid bars 0, 20, 40, ... of each window with forecast < 0) minus the mean forward 20-bar return over all bars of its own window, tested by the ordinary t of the mean. The minimum counts require both 6 short blocks and 120 short bars. The slope regresses forward 20-bar return on |forecast| over all short bars.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
