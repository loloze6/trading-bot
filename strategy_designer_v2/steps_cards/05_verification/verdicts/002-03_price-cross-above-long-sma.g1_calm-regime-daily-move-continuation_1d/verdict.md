---
plan: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d
idea: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 5-bar return on calm grid bars: 0.0100598; t of the mean: 3.31392 (threshold: confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2)
- Supporting check: calm mean minus high-vol mean of the product: None, passed: None
- Counts: calm grid cases: 1793, high-vol grid cases: 0
- Decided by: t >= 2 but the supporting check fails (difference not above 0), which the plan calls inconclusive.
- Reading: Calm bars are grid bars with regime 'trending' and high-vol bars the other grid bars; the coin's mean 5-bar return is the mean of its non-overlapping grid returns over all windows; calm bars with zero forecast are kept as zero products; the high-vol product uses the recorded standardised scaled_day value in place of the forecast, i.e. (value / 10) x excess return; the 100-case minimum is counted on calm grid bars with a valid 5-bar return.
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d`
Measure: `measure.py`
