---
plan: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d
idea: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed next 7-bar return on scaled_move post_pipeline_value: 0.00135928; t of the OLS slope: 4.20943 (threshold: confirm if t >= 2 (with supporting check passing); reject if t <= -2)
- Supporting check: mean drift-removed 7-bar return in forecast direction, before costs: 0.0135488, passed: True
- Counts: active grid bars across all coins and windows: 1114
- Decided by: The slope's t is 2 or more and the mean directional drift-removed return is above 0.
- Reading: Situation checked on active bars with at least 30 earlier bars in their window (ER and r30 recomputed from closes, side = sign of the recorded raw scaled_move, i.e. of r7, continuation expected); drift is the coin's mean 7-bar return on the 7-bar grid of all its windows; the slope t is the OLS t of drift-removed return on post_pipeline_value; the plan's minimum of 40 active grid bars is treated as a minimum count (not observable if unmet).
- Size: unusual move +1.16 % (t 3.01, the cases of one day together: 1038 days) per case over 7 bars, 0.088 of the coin's usual move (12.44 %); normal drift in its direction -0.03 %, total +1.13 %; 1739 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.000278 on the check folds against +0.001359 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d`
Measure: `measure.py`
