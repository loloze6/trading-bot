---
plan: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 24-bar return of settlement-fall cases (forecast >= 2): 0.00240414; ordinary t of case excess returns: 4.16131 (threshold: confirm: weighted mean > 0 with t >= 2 (and supporting check passes); reject: weighted mean < 0 with t <= -2)
- Supporting check: mean excess return of forecast >= 10 cases minus forecast 2 to <10 cases: -0.000206458, passed: False
- Counts: cases: 8564, cases forecast >= 10: 6034, cases forecast 2 to below 10: 2530
- Decided by: A confirming weighted mean and t, but the supporting check failed or could not be measured: inconclusive.
- Reading: Settlement bars are those whose close (timestamp + 1h) is at 00:00 or 16:00 UTC; in each 24-bar grid cell counted from a window's first row the bar with the largest forecast is the case and is dropped if its 24-bar return leaves the window; the coin's mean 24-bar return is taken on the non-overlapping grid of all its windows; the supporting check is the difference of the two groups' unweighted mean excess returns (>=10 minus 2 to <10).
- Size: unusual move +0.16 % per case over 24 bars, 0.031 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.30 %; 8577 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h`
Measure: `measure.py`
