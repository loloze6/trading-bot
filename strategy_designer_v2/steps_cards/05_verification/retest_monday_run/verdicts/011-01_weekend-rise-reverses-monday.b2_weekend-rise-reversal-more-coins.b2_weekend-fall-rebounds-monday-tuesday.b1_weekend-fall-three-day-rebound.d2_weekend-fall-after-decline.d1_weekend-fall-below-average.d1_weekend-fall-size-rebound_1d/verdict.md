---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.d1_weekend-fall-size-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.d1_weekend-fall-size-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (excess 3-bar return x forecast / 10) over Sunday cases with forecast > 0: 0.0110167; t of the mean: 4.03076 (threshold: confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2; at least 100 cases)
- Supporting check: correlation of forecast with excess 3-bar return across cases: 0.0480107, passed: True
- Counts: cases: 1497
- Decided by: The mean of the products is above 0 with t >= 2 and the correlation is above 0.
- Reading: The situation is a bar opening on Sunday UTC whose close is below the 50-bar SMA of closes computed inside its window and whose one-bar return (the recorded raw component, else the close versus the previous day's close) is negative, active Sunday bars whose SMA50 cannot be computed inside the window are left out of the agreement; the coin's mean 3-bar return is taken on the non-overlapping grid (positions 0, 3, 6, ...) of all its windows pooled, cases without 3 bars left in their window are left out, and t is the ordinary t of the mean of the products.
- Size: unusual move +1.19 % per case over 3 bars, 0.138 of the coin's usual move (9.14 %); normal drift in its direction +0.49 %, total +1.69 %; 1297 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.d1_weekend-fall-size-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.d1_weekend-fall-size-rebound_1d`
Measure: `measure.py`
