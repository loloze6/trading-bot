---
plan: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move / coin's usual 5-bar move, forecast < 0 grid bars: 0.0748317; t of the mean: 2.67463 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting check passes); reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: |forecast|-weighted mean of the same unusual move > 0: 0.0687032, passed: True
- Counts: cases: 928, active bars: 4872
- Decided by: Mean above 0 with t >= 2 over at least 30 cases, and the |forecast|-weighted mean is above 0.
- Reading: Situation recomputed per window from prices (net move = |close[t]-close[t-30]| over the 30-bar high-low range, close below the 30-bar high-low midpoint), falling back on the recorded regime where a window lacks 30 bars of history, with the fall read from the sign of fall_lin's raw value; the coin's normal drift and usual move are the mean and standard deviation of its 5-bar returns on the non-overlapping grid of all its windows, and cases are grid bars with forecast < 0 and a close 5 bars later in the same window.
- Size: unusual move +0.55 % per case over 5 bars, 0.049 of the coin's usual move (12.45 %); normal drift in its direction -0.79 %, total -0.24 %; 1710 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d`
Measure: `measure.py`
