---
plan: 044-01_rising-market-wide-down-day-rebound_1d
idea: 044-01_rising-market-wide-down-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-day return of bet cases (coin return minus coin's mean 3-day return): 0.0021228; t of the mean, clustered by day: 0.609379 (threshold: confirm: mean > 0 with day-clustered t >= 2 over >= 100 cases and slope check passes; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: OLS slope of excess 3-day return on range_std post_pipeline_value (positive, t >= 1): 0.00148291, passed: True
- Counts: cases: 1813, days: 863
- Decided by: The main t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: The situation is checked as a close below the prior close within the window on long bars (the rising profile is applied by code not recorded, so it is not recomputed, and each window's first bar, having no prior close, is left out); a case is the first bet (forecast rise >= 2 points from its lowest level since the last bet, reset at 0 after a flat) in each 3-bar grid cell from each window's first row; the coin's mean 3-day return is over the same non-overlapping grid pooled across all its windows; the day-clustered t uses the sum of deviations per signal day with a G/(G-1) correction.
- Size: unusual move +0.21 % (t 0.61, the cases of one day together: 863 days) per case over 3 bars, 0.028 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.57 %; 1813 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/044-01_rising-market-wide-down-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/044-01_rising-market-wide-down-day-rebound_1d`
Measure: `measure.py`
