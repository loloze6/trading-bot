---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-day return after Sunday bars with forecast > 0: 0.012718; t of the mean: 4.84349 (threshold: t >= 2 with slope > 0 (confirm), t <= -2 (reject), on at least 100 cases)
- Supporting check: OLS slope of excess 3-day return on forecast: 0.00137169, passed: True
- Counts: cases: 1427
- Decided by: Mean excess 3-day return positive with t >= 2 on at least 100 cases and a positive slope.
- Reading: A Sunday bar is one whose next calendar day is a Monday (UTC), a case needs close[t+3] in the same window, and the coin's mean 3-day return is taken on the non-overlapping grid 0, 3, 6, ... of all its windows pooled; fewer than 100 cases is reported as not observable.
- Size: unusual move +1.50 % per case over 3 bars, 0.170 of the coin's usual move (9.14 %); normal drift in its direction +0.49 %, total +1.98 %; 1233 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d`
Measure: `measure.py`
