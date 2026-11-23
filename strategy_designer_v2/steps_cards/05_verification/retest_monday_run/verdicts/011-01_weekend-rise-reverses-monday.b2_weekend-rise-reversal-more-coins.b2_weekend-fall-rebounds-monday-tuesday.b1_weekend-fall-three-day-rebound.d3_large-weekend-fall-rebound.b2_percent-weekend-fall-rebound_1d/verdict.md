---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 3-day return on Sunday forecast: 0.0016436; OLS slope t: 4.875 (threshold: confirm: slope > 0 with t >= 2 (and mean drift-adjusted return > 0); reject: slope < 0 with t <= -2; at least 100 cases)
- Supporting check: mean drift-adjusted 3-day return of cases > 0: 0.00604561, passed: True
- Counts: cases: 2547, coins: 19
- Decided by: The slope is positive with t >= 2 and the cases' mean drift-adjusted 3-day return is above 0.
- Reading: Sunday bars are those whose UTC timestamp is a Sunday; the situation is a Sunday with a negative raw 1-bar return (last_history_value, or the price return where missing) and a positive forecast; the coin's drift is the mean of non-overlapping 3-bar returns on each window's grid from its first row over all windows; cases need t+3 inside the window; the plan's 'fewer than 100 cases' is reported as not observable.
- Size: unusual move +0.83 % per case over 3 bars, 0.101 of the coin's usual move (9.20 %); normal drift in its direction +0.45 %, total +1.28 %; 2105 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d`
Measure: `measure.py`
