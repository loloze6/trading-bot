---
plan: 012-04_flush-depth-retracement-size_1d
idea: 012-04_flush-depth-retracement-size
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope t of excess 3-bar forward return on forecast, flush bars: -0.00285778; OLS slope t: -0.721117 (threshold: confirm if slope t >= 2 with forecast-weighted mean excess > 0; reject if slope t <= -2)
- Supporting check: forecast-weighted mean excess 3-bar return > 0: 0.00158289, passed: True
- Counts: independent flush cases: 84
- Decided by: The slope's t lies between -2 and 2.
- Reading: Detector components recomputed from each window's own prices (return z accepted under any of the std variants with/without the current bar and ddof 0/1; volume over the median of the prior 20 bars; lower wick = (min(open,close)-low)/(high-low)), active bars without 20 bars of in-window history left out of the agreement; the coin's mean 3-bar return is taken on the non-overlapping grid (positions 0,3,6,...) of all its windows pooled; flush cases are bars with regime mean_reversion and forecast > 0 and a 3-bar forward return inside the window, skipping any within 3 bars after a counted one in the same window, pooled across coins for one OLS; the plan's 'fewer than 20 independent flush cases' minimum is reported as not observable.
- Size: unusual move +0.20 % per case over 3 bars, 0.033 of the coin's usual move (7.96 %); normal drift in its direction +0.35 %, total +0.55 %; 86 cases
Plan: `steps_cards/03_test_plan/night_012_run/plans/012-04_flush-depth-retracement-size_1d.md`
Record: `steps_cards/04_backtest/night_012_run/backtests/012-04_flush-depth-retracement-size_1d`
Measure: `measure.py`
