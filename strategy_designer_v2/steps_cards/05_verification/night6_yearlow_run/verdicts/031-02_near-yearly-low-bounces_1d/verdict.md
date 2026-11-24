---
plan: 031-02_near-yearly-low-bounces_1d
idea: 031-02_near-yearly-low-bounces
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope t of excess 20-bar return on forecast, pooled non-overlapping cases: -0.00235943; OLS slope t: -1.7029 (threshold: confirm: slope > 0 with t >= 2.0 and top-minus-bottom fifth > 0; reject: slope < 0 with t <= -2.0; otherwise inconclusive; at least 200 cases and 40 in the top fifth)
- Supporting check: mean excess 20-bar return, top fifth minus bottom fifth of forecast: -0.0491256, passed: False
- Counts: independent 20-bar cases: 806, cases in the top fifth: 162, cases in the bottom fifth: 162
- Decided by: Inconclusive rule: the slope t is between -2.0 and 2.0.
- Reading: Fifths are cut at the pooled 20th and 80th percentiles of the cases' forecasts (top: forecast >= 80th percentile, bottom: <= 20th, ties included), cases are the bars at positions 0, 20, 40, ... of each window with the 20-bar return inside the window, and the coin's mean 20-bar return is taken over these grid cases of all its windows.
- Size: unusual move +1.41 % (t 0.75, the cases of one day together: 243 days) per case over 20 bars, 0.063 of the coin's usual move (21.24 %); normal drift in its direction +3.03 %, total +4.44 %; 394 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-02_near-yearly-low-bounces_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02_near-yearly-low-bounces_1d`
Measure: `measure.py`
