---
plan: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-72-bar excess return on raw residual, risen grid bars: 0.0293748; OLS slope t: 3.10884 (threshold: confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; else inconclusive; at least 200 risen grid cases)
- Supporting check: none
- Counts: risen grid cases pooled across coins: 2865
- Decided by: The slope is positive with t >= 2.0: the future excess rise grows as the top-3 share falls.
- Reading: Active bars in each window's first 72 rows (no past 72-bar return computable from the record) are left out of the situation check; the grid is positions 0, 72, 144, ... of each window, so position 0 has no past return and drops out; the coin's mean 72-bar return is the mean of all its grid forward returns over all windows; the slope's t is the ordinary OLS t (slope / standard error); fewer than 200 risen grid cases is reported as not observable.
- Size: unusual move +0.42 % per case over 72 bars, 0.049 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.83 %; 2861 cases
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h`
Measure: `measure.py`
