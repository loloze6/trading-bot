---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 2-bar return of Sunday cases with forecast > 0: 0.00573384; t of the mean of per-Sunday cross-coin means: -0.5531 (threshold: confirm: > 0 with t >= 2 and slope > 0; reject: < 0 with t <= -2)
- Supporting check: OLS slope of excess 2-bar return on forecast: 0.000823107, passed: True
- Counts: Sundays carrying a case: 346, cases: 2664
- Decided by: the numbers meet neither the confirm nor the reject rule (t between -2 and 2, or sign and t disagree).
- Reading: Sunday bar = bar whose UTC start timestamp is a Sunday; the coin's mean 2-bar return is taken on the non-overlapping grid (positions 0, 2, 4, ...) of all its windows pooled; cases without 2 later bars in the window are dropped; the t uses the unweighted cross-coin mean of excess returns per Sunday; the slope is an ordinary least-squares fit of excess return on forecast over all cases.
- Size: unusual move +0.36 % per case over 2 bars, 0.054 of the coin's usual move (7.48 %); normal drift in its direction +0.31 %, total +0.68 %; 2253 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d`
Measure: `measure.py`
