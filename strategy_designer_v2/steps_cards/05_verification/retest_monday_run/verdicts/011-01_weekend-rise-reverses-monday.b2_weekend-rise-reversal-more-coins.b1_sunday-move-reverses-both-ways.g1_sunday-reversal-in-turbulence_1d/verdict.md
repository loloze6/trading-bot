---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 2-bar unusual move on forecast: 0.000737589; OLS slope t: 6.9097 (threshold: slope > 0 with t >= 2 (and check passing) to confirm; slope < 0 with t <= -2 to reject)
- Supporting check: forecast-weighted mean unusual move in forecast direction > 0: 0.00956011, passed: True
- Counts: Sunday cases: 5169
- Decided by: The slope is positive with t >= 2 and the forecast-weighted mean unusual move is above 0.
- Reading: Cases are Sunday-stamped bars (UTC weekday 6) with a non-zero forecast and a close two bars later in the same window; the normal 2-bar drift is the coin's mean 2-bar return on the non-overlapping grid (positions 0, 2, 4, ...) of all its windows pooled; the slope is ordinary least squares with an intercept over all coins pooled, with its usual t; the plan's 'fewer than 300 cases' outcome is reported as 'not observable' per the workflow's minimum-count rule; the situation's side is against Sunday's one-bar close-to-close return (the raw component value when the previous close is not in the window).
- Size: unusual move +0.73 % per case over 2 bars, 0.101 of the coin's usual move (7.48 %); normal drift in its direction +0.01 %, total +0.74 %; 4126 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d`
Measure: `measure.py`
