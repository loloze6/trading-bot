---
plan: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of forecast/10 x excess 24-bar return on the 24-bar grid: 0.00226274; ordinary t of the mean: 4.88902 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 1,000 independent cases)
- Supporting check: top-fifth minus bottom-fifth |forecast| mean of sign(forecast) x excess 24-bar return: 0.00509082, passed: True
- Counts: independent cases: 17246, top fifth cases: 3452, bottom fifth cases: 3447
- Decided by: Pooled mean positive with t >= 2 over at least 1,000 cases, and the top-fifth minus bottom-fifth Welch t is >= 2.
- Reading: The coin's mean 24-bar return is the mean of its grid returns over all windows; the top and bottom fifths are the rank-based top and bottom 20% of grid bars by |forecast| within each coin, pooled across coins; the supporting check passes when that difference is positive with Welch t >= 2; too few cases are reported as not observable.
- Size: unusual move +0.05 % per case over 24 bars, 0.012 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.05 %; 17043 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h`
Measure: `measure.py`
