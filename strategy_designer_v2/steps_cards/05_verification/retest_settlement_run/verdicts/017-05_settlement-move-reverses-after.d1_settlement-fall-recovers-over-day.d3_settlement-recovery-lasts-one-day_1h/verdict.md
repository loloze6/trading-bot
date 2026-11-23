---
plan: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 24-bar forward return on forecast: 0.000199709; OLS slope t: 3.76772 (threshold: positive slope with t >= 2 confirms (with second-day check), negative with t <= -2 rejects)
- Supporting check: second-day (t+24 to t+48) slope t below 2: 0.502727, passed: True
- Counts: cases with forecast > 0: 8534, cases: 17227, second-day cases: 17084
- Decided by: Main slope positive with t >= 2 over at least 200 cases with forecast > 0, and the second-day slope's t is below 2.
- Reading: Cases are the first regime 'mean_reversion' bar in each 24-row grid cell from each window's first row, all such cases (forecast 0 included) enter the regression, the drift is the coin's mean non-overlapping 24-bar return over all windows (used for both days), and the second-day regression uses those cases whose t+48 close lies in the same window.
- Size: unusual move +0.09 % per case over 24 bars, 0.018 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.23 %; 11281 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h`
Measure: `measure.py`
