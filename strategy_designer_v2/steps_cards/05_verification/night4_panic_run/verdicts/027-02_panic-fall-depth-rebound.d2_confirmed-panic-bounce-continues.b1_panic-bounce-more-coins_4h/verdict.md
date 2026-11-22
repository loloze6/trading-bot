---
plan: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
fit: exact
status: inconclusive
---
Situation check: 90 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 84-bar excess return on raw 24h bounce, pooled over coins and windows: 0.000613591; OLS slope t: 1.47327 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 30 cases)
- Supporting check: none
- Counts: cases: 463
- Decided by: t = 1.47 lies between -2 and 2 on 463 cases (inconclusive rule).
- Reading: Panic recomputed as the 6-bar high-low range over its 180-bar mean (min 30 bars where history is short) for bars t-11..t-6 with close[t-6] < close[t-12], long side, on active bars where it is computable; cases are the first regime == 'mean_reversion' bar in each 84-bar grid cell from each window's first row, the coin's mean 84-bar return is taken on the non-overlapping grid of all its windows, the slope and its t are from ordinary least squares, and fewer than 30 cases is read as 'not observable'.
- Size: unusual move -1.28 % per case over 84 bars, -0.041 of the coin's usual move (22.11 %); normal drift in its direction +2.95 %, total +1.68 %; 387 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h`
Measure: `measure.py`
