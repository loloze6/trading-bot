---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of (excess 3-bar return x forecast/10) over Sunday cases: 4.12066; t of the mean: 4.12066 (threshold: t >= 2 over at least 100 cases (confirm, with slope > 0); t <= -2 over at least 100 cases (reject))
- Supporting check: OLS slope of excess 3-bar return on forecast > 0: 0.00161637, passed: True
- Counts: cases: 1493
- Decided by: Confirm: t >= 2 over at least 100 cases and the slope of excess return on forecast is above 0.
- Reading: A Sunday bar is one whose UTC start timestamp is a Sunday (its next bar is a Monday); the coin's mean 3-bar return is pooled over non-overlapping 3-bar stretches of all its windows; cases whose 3-bar return would leave the window are dropped; the minimum of 100 cases gives 'not observable' when unmet.
- Size: unusual move +1.02 % per case over 3 bars, 0.118 of the coin's usual move (9.14 %); normal drift in its direction +0.48 %, total +1.50 %; 1433 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d`
Measure: `measure.py`
