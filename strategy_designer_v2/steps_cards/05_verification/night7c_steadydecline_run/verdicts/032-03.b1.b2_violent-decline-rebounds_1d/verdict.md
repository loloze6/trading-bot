---
plan: 032-03.b1.b2_violent-decline-rebounds_1d
idea: 032-03.b1.b2_violent-decline-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of in-regime 5-day excess return on forecast: 0.000428453; OLS slope t: 0.726918 (threshold: slope t >= 2 confirms (with mean excess > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean in-regime 5-day excess return > 0: -0.00673093, passed: False
- Counts: in-regime grid cases pooled over coins and windows: 1013
- Decided by: Inconclusive: the slope's t is between -2 and 2.
- Reading: The 28-day fall is read from fall_depth's last_history_value (recomputed from closes where missing), while the wide-range condition (28-day vs 365-day mean range) cannot be rebuilt from ~120-bar windows so it is taken from the recorded regime 'mean_reversion'; grid bars at positions 0,5,10,... of each window with close[t+5] inside the window, in-regime meaning forecast > 0, coin mean 5-day return over all its grid bars in all windows, slope t from ordinary least squares with intercept.
- Size: unusual move -0.89 % (t -1.42, the cases of one day together: 441 days) per case over 5 bars, -0.067 of the coin's usual move (11.68 %); normal drift in its direction +0.83 %, total -0.07 %; 836 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03.b1.b2_violent-decline-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b1.b2_violent-decline-rebounds_1d`
Measure: `measure.py`
