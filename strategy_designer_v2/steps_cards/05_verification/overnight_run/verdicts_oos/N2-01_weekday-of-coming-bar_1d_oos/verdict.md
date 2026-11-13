---
plan: N2-01_weekday-of-coming-bar_1d_oos
idea: N2-01_weekday-of-coming-bar
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of allocation x (next-bar return - coin mean daily return) on forecast>0 bars: -0.000160119; t of the mean: -0.187742 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise inconclusive; at least 300 active Saturday bars)
- Supporting check: mean Saturday return minus coin all-window mean daily return (t of the mean): 0.00127788, passed: False
- Counts: active Saturday bars: 1046, Saturday bars: 1804
- Decided by: The main-measure t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Saturday bars are the Friday-dated decision bars whose next bar is Saturday (timestamp + 1 day has weekday 5), the allocation is postRebalance_current_allocation, 'the coin's mean daily return over all 24 windows' is read as the mean of all within-window one-bar returns of that coin over every window present in the record, the 300-bar minimum counts forecast>0 bars with a valid next return, and the supporting check, which has no threshold in the plan, is marked passed when its mean is positive with t >= 2 like the confirm rule.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N2-01_weekday-of-coming-bar_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-01_weekday-of-coming-bar_1d_oos`
Measure: `measure.py`
