---
plan: N4-04_dip-rebound-spans-days_1d_oos2
idea: N4-04_dip-rebound-spans-days
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess return close t+1 to close t+3 after top-decile positive forecasts: 0.0111214; t of the mean: 1.31834 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; fewer than 30 non-overlapping cases is not observable)
- Supporting check: mean 3-bar excess return close t to t+3 vs coin mean 3-bar return, > 0: 0.0357352, passed: True
- Counts: non-overlapping cases: 115, top-decile bars before merging: 169
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: Top decile = positive forecasts at or above the pooled 90th percentile of positive forecasts; the coin's mean 2-bar (and 3-bar) return is taken over every bar of all its windows pooled, each return inside one window; cases on the same coin and window whose bars are at most 3 apart are chained into one case whose value is the mean of its members' excess returns; t is the ordinary t of the mean.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-04_dip-rebound-spans-days_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-04_dip-rebound-spans-days_1d_oos2`
Measure: `measure.py`
