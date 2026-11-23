---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of forecast x excess 3-bar return on Sunday-fall cases: 0.0868012; t of the mean: 4.33584 (threshold: confirm t >= 2 with top-minus-bottom third > 0; reject t <= -2; at least 100 cases)
- Supporting check: top-third minus bottom-third mean excess 3-bar return: 0.0177631, passed: True
- Counts: cases: 2434
- Decided by: t >= 2 and the top-minus-bottom-third difference is above 0.
- Reading: Sunday = UTC bar start on Sunday; cases need 3 bars ahead inside the window; the coin's mean is over its non-overlapping 3-bar grid (0,3,6,... per window) pooled across windows; thirds are the lowest and highest floor(n/3) cases sorted by forecast; the plan's 'fewer than 100 cases' is treated as the minimum count (not observable).
- Size: unusual move +0.78 % per case over 3 bars, 0.100 of the coin's usual move (9.16 %); normal drift in its direction +0.46 %, total +1.24 %; 1825 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d`
Measure: `measure.py`
