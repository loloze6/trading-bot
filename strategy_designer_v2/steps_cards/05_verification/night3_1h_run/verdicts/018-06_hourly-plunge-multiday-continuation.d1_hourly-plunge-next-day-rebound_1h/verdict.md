---
plan: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean strength minus 1 of 24-bar long cases: -0.980247; t of the mean: -86.9172 (threshold: confirm: > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman of case forecast vs unusual move: 0.0426923, passed: True
- Counts: cases: 8426
- Decided by: Mean strength minus 1 is below 0 with t <= -2 over at least 30 cases.
- Reading: Cases are long bets (forecast rises of at least 2 points from its lowest level since the last bet, reset at 0 after a flat), the first per 24-bar grid cell from each window's first row, kept only if 24 bars follow in the window; drift and usual move are the mean and sample std of each coin's non-overlapping 24-bar returns pooled over its windows; the t is the ordinary t of the mean of strength minus 1 over all cases pooled across coins.
- Size: unusual move +0.11 % per case over 24 bars, 0.020 of the coin's usual move (4.87 %); normal drift in its direction +0.15 %, total +0.25 %; 8426 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h`
Measure: `measure.py`
