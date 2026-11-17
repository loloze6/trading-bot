---
plan: 003-02_thin-volume-drop-rebounds_1d
idea: 003-02_thin-volume-drop-rebounds
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return after forecast>0 bars (vs coin's mean 5-bar return): 0.0664532; one-sample t: 1.27244 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 20 independent events)
- Supporting check: OLS slope of excess 5-bar return on forecast: -0.0279252, passed: False
- Counts: independent events: 5, bars with forecast above 0: 5
- Decided by: Only 5 independent events, fewer than the plan's minimum of 20.
- Reading: Raw fall size and volume ratio are read from the recorded 'fall' and 'volume' components' last_history_value (recomputed from prices only if missing); the coin's mean 5-bar return is taken on the non-overlapping grid (positions 0,5,10,... of each window) pooled over all windows; an event is dropped when it lies fewer than 5 bars after the previous counted event in the same window, and events without a full 5-bar forward return inside their window are left out.
Plan: `steps_cards/03_test_plan/volume_run/plans/003-02_thin-volume-drop-rebounds_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/003-02_thin-volume-drop-rebounds_1d`
Measure: `measure.py`
