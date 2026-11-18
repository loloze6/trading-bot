---
plan: 012-01_liquidation-flush-rebound_1d
idea: 012-01_liquidation-flush-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 3-bar excess return over the coin's mean, grid bars with forecast >= 2: 0.0101427; t of the mean: 3.26461 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2)
- Supporting check: forecast-weighted mean excess minus unweighted mean excess: 0.000306308, passed: True
- Counts: qualifying grid bars: 919
- Decided by: The mean excess 3-bar return is > 0 with t >= 2, and the forecast-weighted mean exceeds the unweighted mean.
- Reading: The coin's mean 3-bar return is the mean over the same non-overlapping grid (positions 0, 3, 6, ... of each window) pooled over all its windows; the plan's 'fewer than 30 qualifying grid bars' is treated as a minimum count, so it gives 'not observable'; and the situation check rebuilds the fall, the 30-bar volume ratio (current bar included) and the wick from prices.
Plan: `steps_cards/03_test_plan/volume_run/plans/012-01_liquidation-flush-rebound_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/012-01_liquidation-flush-rebound_1d`
Measure: `measure.py`
