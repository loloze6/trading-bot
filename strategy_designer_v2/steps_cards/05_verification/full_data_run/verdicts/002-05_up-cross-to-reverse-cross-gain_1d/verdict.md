---
plan: 002-05_up-cross-to-reverse-cross-gain_1d
idea: 002-05_up-cross-to-reverse-cross-gain
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: Mean 20-bar forward return after forecast > 0 minus mean 20-bar forward return of all bars, non-overlapping blocks, pooled: 0.0084386; Welch t: 0.44134 (threshold: excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects; else inconclusive; fewer than 30 blocks with forecast > 0 is inconclusive)
- Supporting check: Share of positive 20-bar forward returns when forecast > 0 minus unconditional share: -0.0139373, passed: False
- Counts: non-overlapping 20-bar blocks with forecast > 0: 409, non-overlapping 20-bar blocks, all bars: 811
- Decided by: The t-statistic lies between -2 and 2, so the result is inconclusive.
- Reading: Situation is last_history_value > 0 with forecast > 0; blocks start at positions 0, 20, 40, ... of each window with the full 20-bar return inside the window; the comparison group is all grid blocks of all coin-windows pooled, tested with Welch t; the supporting check passes when the conditional hit rate exceeds the unconditional one.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-05_up-cross-to-reverse-cross-gain_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Measure: `measure.py`
