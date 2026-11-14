---
plan: N7-01_drift-only-near-high_1d_oos2
idea: N7-01_drift-only-near-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 5-bar excess return: 0.0339923; weighted t of the mean: 1.39425 (threshold: confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2; else inconclusive; at least 100 active blocks)
- Supporting check: mean 5-bar excess return on flat bars, recent high, close below SMA20 (<= 0): -0.0162254, passed: True
- Counts: non-overlapping active 5-bar blocks: 273, supporting flat blocks: 73, active bars: 1401
- Decided by: The t-statistic lies strictly between -2 and 2 (or could not be computed).
- Reading: Situation taken as the gate (close above SMA20 and a new 20-day closing high within the last 20 bars, long), nearness to the high being graded not gated; the coin's mean 5-bar return uses every bar's 5-bar return in all its windows; the t of the forecast-weighted mean uses the weighted standard error sqrt(sum w^2 (x-m)^2)/sum w; the supporting check uses excess over the coin's mean on grid flat bars and does not enter the decision rule.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N7-01_drift-only-near-high_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N7-01_drift-only-near-high_1d_oos2`
Measure: `measure.py`
