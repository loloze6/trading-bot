---
plan: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-3-bar excess return (vs coin mean 3-bar return) on forecast: 0.00030136; OLS slope t: 2.50845 (threshold: confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; at least 300 nonzero-forecast grid cases)
- Supporting check: none
- Counts: grid cases with a nonzero forecast: 5721, grid cases in regression: 5723
- Decided by: the slope is positive with t >= 2.0 on at least 300 nonzero-forecast grid cases (confirm rule)
- Reading: the regression is OLS with an intercept on all grid cases with a valid next-3-bar return (zero forecasts included); the coin's mean 3-bar return is the mean of its grid returns over all windows; a shortfall of the plan's 300-case minimum is reported as 'not observable' per the workflow
- Size: unusual move +0.60 % per case over 3 bars, 0.070 of the coin's usual move (7.96 %); normal drift in its direction +0.10 %, total +0.71 %; 1994 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d`
Measure: `measure.py`
