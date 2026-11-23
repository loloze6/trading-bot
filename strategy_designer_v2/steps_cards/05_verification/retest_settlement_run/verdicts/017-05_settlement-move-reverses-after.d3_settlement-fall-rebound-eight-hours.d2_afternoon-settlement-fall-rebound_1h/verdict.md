---
plan: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x drift-removed 8-bar return, pooled: 0.0225192; ordinary t: 5.16266 (threshold: mean > 0 with t >= 2 and supporting check passes confirms; mean < 0 with t <= -2 rejects; fewer than 300 cases inconclusive)
- Supporting check: drift-removed 8-bar return, above-median forecast minus below-median: 0.00197649, passed: True
- Counts: cases: 8637, cases above median: 4318, cases below median: 4318
- Decided by: The main-measure mean is > 0 with t >= 2 and the supporting check passes.
- Reading: The settlement bar is the bar whose close (start + 1h) is 16:00 UTC, the 8-bar return is taken 8 rows ahead inside the window, the median is pooled over all cases with cases equal to it left out of both halves, and the 300-case minimum is treated as the plan's minimum count (not observable).
- Size: unusual move +0.19 % per case over 8 bars, 0.064 of the coin's usual move (2.81 %); normal drift in its direction +0.05 %, total +0.23 %; 7499 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h`
Measure: `measure.py`
