---
plan: 012-03_lower-wick-flush-recovery_1d
idea: 012-03_lower-wick-flush-recovery
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope t of excess 3-bar return on wick (post_pipeline_value), pooled: 0.00134916; OLS slope t: 0.772884 (threshold: confirm if slope t >= 2 with supporting check passing; reject if slope t <= -2; at least 30 independent flush bars)
- Supporting check: mean excess 3-bar return of flush bars with wick above flush-bar median > 0: 0.00568398, passed: True
- Counts: independent flush bars: 223
- Decided by: The slope t is between -2 and 2.
- Reading: Situation recomputed as 1-bar return / std (ddof 1) of the last 20 one-bar returns including the bar <= -2 and volume / mean of the prior 20 volumes >= 2, falling back to the recorded regime on bars without 20 bars of in-window history; the coin's mean 3-bar return is taken on the non-overlapping grid (positions 0,3,6,... of every window) pooled over all windows; flush bars are thinned before dropping those without close[t+3] in the window, and the median for the check is over the kept flush bars.
- Size: unusual move -0.14 % per case over 3 bars, 0.006 of the coin's usual move (7.96 %); normal drift in its direction +0.35 %, total +0.21 %; 175 cases
Plan: `steps_cards/03_test_plan/night_012_run/plans/012-03_lower-wick-flush-recovery_1d.md`
Record: `steps_cards/04_backtest/night_012_run/backtests/012-03_lower-wick-flush-recovery_1d`
Measure: `measure.py`
