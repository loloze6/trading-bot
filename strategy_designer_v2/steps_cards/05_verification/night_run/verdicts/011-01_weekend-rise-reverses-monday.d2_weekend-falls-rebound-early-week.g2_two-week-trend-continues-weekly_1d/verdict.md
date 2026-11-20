---
plan: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of forecast x 7-bar excess return (non-overlapping cases): 0.116077; t of the mean: 3.44726 (threshold: confirm: mean > 0 with t >= 2 (and timing part > 0); reject: mean < 0 with t <= -2; at least 300 cases)
- Supporting check: timing part of the book's mean daily return (book mean minus position x coin mean daily return): 0.000516765, passed: True
- Counts: independent 7-bar cases: 2443
- Decided by: The pooled mean of the product is positive with t >= 2 and the timing part of the book's mean daily return is above 0.
- Reading: The coin's mean 7-bar return is the mean over that coin's non-overlapping grid cases pooled across all its windows; the book's daily return is the change in postRebalance_total_value between consecutive day-end bars inside a window, averaged across coins per day, with the market part being the previous day's post-rebalance allocation times the coin's mean daily close return over all windows; the plan's 'fewer than 300 cases' is treated as a minimum count and reported as not observable.
- Size: unusual move +0.44 % per case over 7 bars, 0.030 of the coin's usual move (12.44 %); normal drift in its direction -0.02 %, total +0.42 %; 2207 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d`
Measure: `measure.py`
