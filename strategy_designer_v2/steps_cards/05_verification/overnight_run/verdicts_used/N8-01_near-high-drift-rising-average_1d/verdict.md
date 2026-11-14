---
plan: N8-01_near-high-drift-rising-average_1d
idea: N8-01_near-high-drift-rising-average
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return vs coin mean 5-bar return, forecast > 0: 0.00808172; t of the mean (non-overlapping): 2.28928 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 30 non-overlapping cases)
- Supporting check: OLS slope of excess 5-bar return on forecast: 0.00100517, passed: True
- Counts: non-overlapping in-situation cases: 1214, in-situation bars: 5939, active bars: 6141
- Decided by: Confirm rule met: mean excess 5-bar return is above 0 with t >= 2.
- Reading: Situation recomputed from closes per window (SMA20 5-bar change > 0, close > SMA20, bars-since-20-day-closing-high from the recorded recency value or recomputed > 0), falling back to regime == 'trending' on early rows where it cannot be computed; benchmark is the coin's mean of all overlapping 5-bar returns across its windows; the mean excess return and its ordinary t both use the non-overlapping in-situation bars (positions 0,5,10,... of each window); the supporting slope is OLS of excess return on forecast over all in-situation bars; the 30-case minimum is treated as a minimum count giving 'not observable'.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N8-01_near-high-drift-rising-average_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N8-01_near-high-drift-rising-average_1d`
Measure: `measure.py`
