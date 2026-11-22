---
plan: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 5-bar forward return on forecast, trending grid bars, pooled: 0.00184615; OLS slope t: 2.51081 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 200 independent grid cases)
- Supporting check: none
- Counts: independent trending-regime grid cases: 153
- Decided by: Fewer than 200 independent trending-regime grid cases (153), the plan's minimum.
- Reading: The situation check takes the 90-bar return from the prices where 90 past closes exist in the window and the recorded regime otherwise, and the side from the close's position in its last 30 closes (or the sign of the recorded raw value before 30 closes exist); the main measure uses the recorded regime == 'trending' on the grid bars 0,5,10,... of each window, trending grid bars with forecast 0 included, an OLS with intercept pooled over all coins, and the coin's mean 5-bar return from the same non-overlapping grid of all its windows; fewer than 200 cases is reported as 'not observable'.
- Size: unusual move +1.11 % per case over 5 bars, 0.144 of the coin's usual move (8.48 %); normal drift in its direction +0.16 %, total +1.26 %; 136 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d`
Measure: `measure.py`
