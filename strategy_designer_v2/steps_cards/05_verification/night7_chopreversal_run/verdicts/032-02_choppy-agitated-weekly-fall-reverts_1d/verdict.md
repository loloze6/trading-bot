---
plan: 032-02_choppy-agitated-weekly-fall-reverts_1d
idea: 032-02_choppy-agitated-weekly-fall-reverts
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered slope of 7-bar excess return on forecast (forecast > 0 grid cells): -0.00099226; day-clustered slope t: -0.536329 (threshold: confirm: slope t >= 2 with mean excess > 0; reject: slope t <= -2; at least 30 day-clustered positive-forecast cells)
- Supporting check: mean excess 7-bar return over positive-forecast cells > 0: 0.00202501, passed: True
- Counts: independent positive-forecast grid cells (day-clustered): 70, positive-forecast grid cells: 99
- Decided by: Slope t between -2 and 2: the plan's inconclusive rule.
- Reading: Situation taken as a negative raw 7-bar return (fall7 last_history_value, recomputed from closes where missing) with a positive forecast, the choppy agitated profile being enforced by the regime and not re-checked; grid cells at positions 0,7,14,... of each window with a full 7-bar forward return inside the window; normal drift = mean of the coin's grid 7-bar returns over all its windows; slope from OLS with intercept and day-clustered (CR1) standard error; the 30-cell minimum counted as distinct days, and its shortfall reported as not observable.
- Size: unusual move -0.39 % (t -0.40, the cases of one day together: 171 days) per case over 7 bars, -0.040 of the coin's usual move (12.44 %); normal drift in its direction +0.95 %, total +0.56 %; 209 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/032-02_choppy-agitated-weekly-fall-reverts_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/032-02_choppy-agitated-weekly-fall-reverts_1d`
Measure: `measure.py`
