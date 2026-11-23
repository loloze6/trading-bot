---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar return on forecast, Sunday bars with forecast > 0: 0.00114302; OLS slope t: 1.56678 (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2; at least 200 cases)
- Supporting check: mean excess 3-bar return > 0: 0.00979871, passed: True
- Counts: cases: 524
- Decided by: The slope t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Sunday bars are bars whose UTC start is a Sunday (the next bar is Monday), a weekend fall is a negative raw component value (the Sunday one-bar return where not recorded), cases are those with a full 3-bar return inside the window, the slope's t is the ordinary OLS t, and the plan's 'below 200 cases' rule is applied as the minimum count giving 'not observable'.
- Size: unusual move +1.34 % per case over 3 bars, 0.141 of the coin's usual move (9.47 %); normal drift in its direction +0.44 %, total +1.78 %; 437 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence_1d`
Measure: `measure.py`
