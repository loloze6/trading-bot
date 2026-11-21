---
plan: 002-02_sma-death-cross-downward-drift_1d
idea: 002-02_sma-death-cross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean 10-bar excess gain of the short over holding (holding - forward return), pooled: 0.00149497; t of the weighted mean (effective n): 0.259295 (threshold: confirm if mean > 0 with t >= 2 (and top tercile > bottom tercile); reject if mean < 0 with t <= -2)
- Supporting check: top minus bottom |forecast| tercile weighted excess gain: 0.00647281, passed: True
- Counts: non-overlapping short cases: 825
- Decided by: The t-statistic is strictly between -2 and 2 (or undefined), which the plan calls inconclusive.
- Reading: Active bars whose raw spread is missing are left out of the situation check; holding is the coin's mean 10-bar return on the non-overlapping grid (positions 0,10,20,... of each window) across all its windows; the short's excess gain is holding minus the forward return; the t of the weighted mean uses the weighted standard deviation and Kish's effective n; terciles split the short cases by rank of |forecast| into three near-equal groups, and each tercile's excess is its |forecast|-weighted mean; the plan's 'fewer than 30 short cases' rule is reported as not observable.
- Size: unusual move +0.53 % per case over 10 bars, 0.039 of the coin's usual move (14.49 %); normal drift in its direction -1.31 %, total -0.78 %; 256 cases
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-02_sma-death-cross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-02_sma-death-cross-downward-drift_1d`
Measure: `measure.py`
