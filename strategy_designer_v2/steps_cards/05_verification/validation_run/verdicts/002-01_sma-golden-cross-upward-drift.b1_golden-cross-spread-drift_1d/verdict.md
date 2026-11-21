---
plan: 002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift_1d
idea: 002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-day return on forecast, positive-forecast grid cases: 0.000481999; OLS slope t: 0.742452 (threshold: confirm if slope t >= 2 and forecast-weighted mean excess > 0; reject if slope t <= -2)
- Supporting check: forecast-weighted mean excess 10-day return > 0: 0.000548161, passed: True
- Counts: positive-forecast grid cases: 1567
- Decided by: The slope t is between -2 and 2.
- Reading: The situation is read from the recorded raw spread being above 0 with a positive forecast; the coin's usual 10-bar return is the mean of all its non-overlapping grid returns (positions 0, 10, 20, ...) pooled over its windows, the slope t is the ordinary OLS slope t from scipy linregress, and the plan's 'fewer than 100 cases' rule is treated as a minimum count giving 'not observable'.
- Size: unusual move +2.22 % per case over 10 bars, 0.109 of the coin's usual move (15.92 %); normal drift in its direction +1.34 %, total +3.56 %; 505 cases
Plan: `steps_cards/03_test_plan/plans/002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift_1d`
Measure: `measure.py`
