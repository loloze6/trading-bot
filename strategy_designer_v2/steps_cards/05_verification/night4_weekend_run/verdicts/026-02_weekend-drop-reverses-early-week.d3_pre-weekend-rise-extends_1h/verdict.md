---
plan: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the OLS slope of excess 48-bar return on forecast, Friday 00:00 cases: 0.000721489; OLS slope t: 2.5879 (threshold: confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2)
- Supporting check: forecast-weighted mean excess 48-bar return > 0: 0.010169, passed: True
- Counts: cases across coins and windows: 1161
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: Cases are bars whose close (timestamp + 1h) is Friday 00:00 UTC with forecast > 0 and a full 48-row forward return inside the window; the coin's mean 48-bar return is taken on the non-overlapping grid of all its windows pooled; one pooled OLS across all coins.
- Size: unusual move +0.80 % per case over 48 bars, 0.117 of the coin's usual move (6.56 %); normal drift in its direction +0.27 %, total +1.07 %; 1035 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h`
Measure: `measure.py`
