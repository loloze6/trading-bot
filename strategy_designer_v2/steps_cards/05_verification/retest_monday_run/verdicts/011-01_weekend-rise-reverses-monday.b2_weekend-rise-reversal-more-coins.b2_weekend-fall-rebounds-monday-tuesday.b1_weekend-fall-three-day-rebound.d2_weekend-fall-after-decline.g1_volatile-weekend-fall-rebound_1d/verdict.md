---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar return after Sunday bars with forecast >= 2: 0.0074137; ordinary t of the mean: 3.57749 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: forecast-weighted mean excess minus unweighted mean: 0.00430605, passed: True
- Counts: cases: 2372
- Decided by: Mean excess 3-bar return positive with t >= 2 over at least 100 cases, and the forecast-weighted mean exceeds the unweighted mean.
- Reading: A case is any bar whose UTC start timestamp is a Sunday with forecast >= 2 and a full 3-bar return inside its window, the coin's normal drift is the mean of its 3-bar returns on each window's grid 0,3,6,... over all its windows, and the plan's 'fewer than 100 cases' is reported as not observable per the workflow.
- Size: unusual move +0.74 % per case over 3 bars, 0.088 of the coin's usual move (9.14 %); normal drift in its direction +0.48 %, total +1.22 %; 2373 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d`
Measure: `measure.py`
