---
plan: N7-01_drift-only-near-high_1d_oos3
idea: N7-01_drift-only-near-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean forward 5-bar excess return over the coin mean: 0.00136867; t of the mean weighted excess return: 0.122837 (threshold: confirm if positive with t >= 2, reject if negative with t <= -2, else inconclusive)
- Supporting check: mean forward 5-bar excess return on flat bars with recent high but close below SMA20 <= 0: -0.00910738, passed: True
- Counts: non-overlapping active 5-bar blocks: 155, supporting flat blocks: 66
- Decided by: The t-statistic lies strictly between -2 and 2.
- Reading: Situation recomputed from prices (close above its 20-bar SMA and a close at or above the prior 20 closes' max within the last 20 bars, with the recorded recency raw value > 0 used where the window's prices are too short), active bars without a computable SMA left out; the coin mean 5-bar return is taken over all of the coin's bars in all its windows; blocks are the window grid positions 0,5,10,... with an active forecast; the t is the ordinary t of the forecast-weighted excess returns (same sign as the weighted mean); the supporting check uses the same grid and excess over the coin mean and does not enter the decision rule.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N7-01_drift-only-near-high_1d_oos3.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N7-01_drift-only-near-high_1d_oos3`
Measure: `measure.py`
