---
plan: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d
idea: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed next 7-bar return on scaled_move post_pipeline_value: 0.00145408; t of the OLS slope: 1.20237 (threshold: confirm if t >= 2 (with supporting check passing); reject if t <= -2)
- Supporting check: mean drift-removed 7-bar return in forecast direction, before costs: -0.00128487, passed: False
- Counts: active grid bars across all coins and windows: 154
- Decided by: The slope's t is strictly between -2 and 2.
- Reading: Situation checked on active bars with at least 30 earlier bars in their window (ER and r30 recomputed from closes, side = sign of the recorded raw scaled_move, i.e. of r7, continuation expected); drift is the coin's mean 7-bar return on the 7-bar grid of all its windows; the slope t is the OLS t of drift-removed return on post_pipeline_value; the plan's minimum of 40 active grid bars is treated as a minimum count (not observable if unmet).
- Size: unusual move +1.67 % (t 1.28, the cases of one day together: 170 days) per case over 7 bars, 0.066 of the coin's usual move (22.86 %); normal drift in its direction +1.00 %, total +2.67 %; 227 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/unseen_2016_2017/backtests/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d`
Measure: `measure.py`
