---
plan: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 72-bar forward return, grind group minus jump group: 0.00471131; Welch t: 0.827359 (threshold: confirm: difference > 0 with Welch t >= 2; reject: difference < 0 with Welch t <= -2; at least 200 grid cases per group)
- Supporting check: none
- Counts: grind group grid cases: 487, jump group grid cases: 490
- Decided by: The Welch t is between -2 and 2 (or its sign disagrees with the difference), which the plan calls inconclusive.
- Reading: The sample is the grid bars (positions 0, 72, 144, ... of each window) with raw grind_residual above 0 and a 72-bar forward return inside the window; the per-coin median is taken over that coin's sample across all its windows; the plan's 200-case minimum, when not met, is reported as not observable.
- Size: unusual move +0.43 % per case over 72 bars, 0.049 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.83 %; 2862 cases
Plan: `steps_cards/03_test_plan/hold_ideas_1h_run/plans/016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h.md`
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h`
Measure: `measure.py`
