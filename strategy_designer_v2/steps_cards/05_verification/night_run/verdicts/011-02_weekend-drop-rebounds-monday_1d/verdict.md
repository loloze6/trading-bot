---
plan: 011-02_weekend-drop-rebounds-monday_1d
idea: 011-02_weekend-drop-rebounds-monday
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean forecast/10 x excess 2-bar return over Sunday cases, pooled: 0.00273526; t of the mean: 1.34532 (threshold: confirm if t >= 2 with the check passing; reject if t <= -2; at least 100 cases with forecast > 0)
- Supporting check: top third minus bottom third mean excess 2-bar return: 0.0024608, passed: True
- Counts: cases with forecast > 0: 1197
- Decided by: The main t is between -2 and 2.
- Reading: Cases are bars with regime 'trending' and forecast > 0 whose t+2 close lies in the same window; thirds are n//3 cases each, ranked by forecast; the plan's 'fewer than 100 cases' is treated as the minimum count (not observable); the situation check identifies days from the UTC start timestamp.
- Size: unusual move +0.30 % per case over 2 bars, 0.050 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.54 %; 1023 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-02_weekend-drop-rebounds-monday_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-02_weekend-drop-rebounds-monday_1d`
Measure: `measure.py`
