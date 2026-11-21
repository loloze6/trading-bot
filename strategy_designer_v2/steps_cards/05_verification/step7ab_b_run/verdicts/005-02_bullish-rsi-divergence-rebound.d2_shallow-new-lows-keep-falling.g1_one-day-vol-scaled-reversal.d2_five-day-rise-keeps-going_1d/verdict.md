---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the demeaned 3-bar forward return on the forecast (non-overlapping grid, pooled): 3.44679; OLS slope t: 3.44679 (threshold: confirm if slope t >= 2 with a positive supporting check; reject if slope t <= -2)
- Supporting check: mean unusual 3-bar move of grid bars with forecast > 0: 0.0018228, passed: True
- Counts: grid bars with forecast > 0: 1024, grid bars in total: 1907
- Decided by: Confirm rule met: slope t >= 2 and the mean unusual move of forecast > 0 grid bars is above 0.
- Reading: The coin's mean 3-bar return is taken on the same non-overlapping grid pooled over all its windows, grid bars without a full 3-bar forward return in their window are dropped, the slope t is the ordinary OLS t on the pooled grid, and the plan's 'inconclusive with too few bars' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.25 % per case over 3 bars, 0.038 of the coin's usual move (6.82 %); normal drift in its direction +0.39 %, total +0.63 %; 913 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d`
Measure: `measure.py`
