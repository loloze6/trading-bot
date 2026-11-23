---
plan: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 8-bar return after settlement cases: 0.000256955; t of the mean: 1.2507 (threshold: confirm if t >= 2 (with positive slope); reject if t <= -2)
- Supporting check: slope of signed excess return on |forecast|: 0.000178282, passed: True
- Counts: cases: 17689
- Decided by: t is between -2 and 2.
- Reading: Settlement bars are those whose close (timestamp + 1h) falls at 00:00, 08:00 or 16:00 UTC; returns, the 2-bar pre-move and the 24-bar trend are taken by row position inside each window (trend from the recorded raw component where present, else from prices); cases without a full 8-bar return inside their window are dropped; the 100-case minimum is applied as 'not observable'.
- Size: unusual move +0.02 % per case over 8 bars, 0.007 of the coin's usual move (2.81 %); normal drift in its direction +0.00 %, total +0.02 %; 17729 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h`
Measure: `measure.py`
