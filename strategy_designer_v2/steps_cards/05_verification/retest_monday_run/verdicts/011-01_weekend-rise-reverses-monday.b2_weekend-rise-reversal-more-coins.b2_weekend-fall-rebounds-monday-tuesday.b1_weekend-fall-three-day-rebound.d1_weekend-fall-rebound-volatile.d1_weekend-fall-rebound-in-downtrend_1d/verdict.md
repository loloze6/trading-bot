---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar return of Sunday cases (return minus coin's normal 3-bar drift): 0.012718; ordinary t of the mean: 4.84349 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: mean unusual 3-bar return above median forecast minus below median: 0.0204508, passed: True
- Counts: cases: 1427
- Decided by: Mean unusual 3-bar return positive with t >= 2 over at least 100 cases, and the supporting check above 0.
- Reading: Situation bars are Sunday-start daily bars (next bar Monday) whose recorded raw component is > 0 (or, where unrecorded, one-bar and 20-bar price returns both negative) with forecast > 0; cases need close[t+3] inside the same window; cases equal to the median forecast are left out of both supporting groups.
- Size: unusual move +1.50 % per case over 3 bars, 0.170 of the coin's usual move (9.14 %); normal drift in its direction +0.49 %, total +1.98 %; 1233 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend_1d`
Measure: `measure.py`
