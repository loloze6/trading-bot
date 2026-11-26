---
plan: 062-02_choppy-calm-below-high-falls_1d
idea: 062-02_choppy-calm-below-high-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess forward return on forecast, day-pooled: -0.00033653; OLS t of slope on day cases: -0.441104 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 5-bar return on grid bars with forecast <= -10 below 0: -0.00970044, passed: True
- Counts: distinct days of grid cases with non-zero forecast: 233, grid cases with non-zero forecast: 425, grid cases with forecast <= -10: 232
- Decided by: The slope's |t| is below 2, which the plan rules inconclusive.
- Reading: Day pooling is read as averaging the forecast and excess return of the grid cases sharing a UTC day into one case and regressing those day means by OLS (t on n_days-2 df), the drift is each coin's mean 5-bar return over all grid bars of all its windows, the supporting check is the plain mean over grid bars, and the plan's 50-day minimum, when unmet, gives 'not observable' per the workflow.
- Size: unusual move +0.65 % (t 1.81, the cases of one day together: 492 days) per case over 5 bars, 0.074 of the coin's usual move (10.60 %); normal drift in its direction -0.62 %, total +0.02 %; 691 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/062-02_choppy-calm-below-high-falls_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/062-02_choppy-calm-below-high-falls_1d`
Measure: `measure.py`
