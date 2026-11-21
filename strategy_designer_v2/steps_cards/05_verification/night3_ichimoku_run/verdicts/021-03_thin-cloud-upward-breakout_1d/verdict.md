---
plan: 021-03_thin-cloud-upward-breakout_1d
idea: 021-03_thin-cloud-upward-breakout
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 26-bar return at upward cloud crosses: 0.0486939; t of the mean: 1.54603 (threshold: confirm: mean > 0 with t >= 2; reject: t <= -2; at least 30 cases)
- Supporting check: thin minus thick cloud mean unusual 26-bar return (Welch t): 0.0023252, passed: False
- Counts: cross cases: 152, thin group cases: 76, thick group cases: 76
- Decided by: inconclusive rule: neither the confirm nor the reject rule holds (t between -2 and 2 on at least one measure).
- Reading: the situation is checked on the active bars where the cloud (spans shifted 26 bars) can be recomputed from the window's own recorded bars, a cross being a close above the cloud whose last non-inside state before was below it; cases are bars with regime 'trending' whose 26-bar return stays inside the window, at most one per 26-bar grid cell of each window (the first), the drift is the coin's mean non-overlapping 26-bar return over all its windows, groups are strictly above and strictly below the cases' median thin_cloud post_pipeline_value, and the plan's too-few-cases clause is reported as 'not observable'.
- Size: unusual move +5.04 % per case over 26 bars, 0.150 of the coin's usual move (25.48 %); normal drift in its direction +4.40 %, total +9.44 %; 151 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout_1d`
Measure: `measure.py`
