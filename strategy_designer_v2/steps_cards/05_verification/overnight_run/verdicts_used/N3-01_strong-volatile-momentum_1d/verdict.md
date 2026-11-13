---
plan: N3-01_strong-volatile-momentum_1d
idea: N3-01_strong-volatile-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after forecast >= 10 (vs coin mean): 0.00968343; t of the mean: 1.3753 (threshold: positive with t >= 2 confirms; negative with t <= -2 rejects; otherwise inconclusive)
- Supporting check: slope of excess 5-bar return on forecast, active bars, non-overlapping: 0.000427549, passed: True
- Counts: non-overlapping cases at forecast >= 10: 369
- Decided by: The t-statistic is between -2 and 2 (inconclusive rule).
- Reading: Situation checked on the 'regime' column (detector components not recorded) plus ret20 > 0 where recorded; cases and the coin's mean 5-bar return both use the non-overlapping grid (positions 0,5,10,... of each window) pooled over all windows; the supporting check is reported but does not change the status.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N3-01_strong-volatile-momentum_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-01_strong-volatile-momentum_1d`
Measure: `measure.py`
