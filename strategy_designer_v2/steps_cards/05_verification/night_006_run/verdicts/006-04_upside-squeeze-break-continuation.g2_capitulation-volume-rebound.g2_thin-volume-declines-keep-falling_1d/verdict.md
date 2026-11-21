---
plan: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d
idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 3-bar forward return on forecast, mean_reversion grid bars: 0.000384232; OLS slope t: 2.74083 (threshold: confirm if t >= 2 with supporting check passed; reject if t <= -2; else inconclusive; at least 100 grid cases)
- Supporting check: mean excess 3-bar return on grid bars with forecast < 0 below 0: -0.00531478, passed: True
- Counts: grid cases in the regime: 2815, grid cases with forecast < 0: 1752
- Decided by: The slope's t is >= 2 and the mean excess 3-bar return on forecast < 0 grid bars is below 0.
- Reading: Expected side read as the graded relation (short when the 5/30 log volume ratio is below 0, long when above), situation recomputed as close/close[-5]-1 < 0 with the recorded regime used on each window's first 5 bars; the coin's mean 3-bar return is taken over its non-overlapping grid bars of all windows, and the regression is pooled over coins.
- Size: unusual move +0.32 % per case over 3 bars, 0.034 of the coin's usual move (7.96 %); normal drift in its direction -0.11 %, total +0.21 %; 2858 cases
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d`
Measure: `measure.py`
