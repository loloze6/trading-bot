---
plan: N4-04_dip-rebound-spans-days_1d_oos
idea: N4-04_dip-rebound-spans-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess return close t+1 to close t+3 after top-decile positive forecasts: 0.014188; t of the mean: 3.56324 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 30 non-overlapping cases)
- Supporting check: mean 3-bar excess return (close t to t+3) vs coin mean 3-bar return, should be > 0: 0.0194987, passed: True
- Counts: non-overlapping cases: 291, top-decile bars before merging: 396
- Decided by: The mean excess return over days 2-3 is above 0 with t >= 2.
- Reading: Situation = regime 'trending' and a negative one-bar return (dip raw value, else close-to-close) with a long forecast; top decile = positive forecasts >= the 90th percentile of all positive forecasts pooled (ties included); coin mean 2-bar and 3-bar returns are over every bar of all its windows, inside windows; cases on the same coin and window whose bars are <= 3 apart are chained into one case whose excess is the mean of its members.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-04_dip-rebound-spans-days_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-04_dip-rebound-spans-days_1d_oos`
Measure: `measure.py`
