---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 2-bar return over coin mean, Sunday cases: 0.00639905; t of the mean: 5.55442 (threshold: confirm if t >= 2 with tercile check passing; reject if t <= -2; at least 300 cases)
- Supporting check: top minus bottom |forecast| tercile mean of sign(forecast) x excess 2-bar return: 0.00537957, passed: True
- Counts: cases: 5238
- Decided by: The main-measure t is >= 2 and the top-minus-bottom tercile difference is > 0.
- Reading: Sunday bar is the bar whose UTC start is a Sunday; side expected is opposite the sign of the Sunday 1-bar return (recorded last_history_value, else close/prev close); cases require Sunday, regime mean_reversion, non-zero forecast and t+2 in window; coin mean 2-bar return from the non-overlapping grid of all windows pooled; terciles are three near-equal groups of cases sorted by |forecast| (stable sort), and the 300-case minimum is treated as the not-observable minimum.
- Size: unusual move +0.71 % per case over 2 bars, 0.097 of the coin's usual move (7.48 %); normal drift in its direction +0.01 %, total +0.72 %; 4388 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d`
Measure: `measure.py`
