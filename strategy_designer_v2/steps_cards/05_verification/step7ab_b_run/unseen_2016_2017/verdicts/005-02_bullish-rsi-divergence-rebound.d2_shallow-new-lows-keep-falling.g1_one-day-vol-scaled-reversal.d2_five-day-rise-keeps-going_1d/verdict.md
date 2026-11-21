---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the demeaned 3-bar forward return on the forecast (non-overlapping grid, pooled): 1.0537; OLS slope t: 1.0537 (threshold: confirm if slope t >= 2 with a positive supporting check; reject if slope t <= -2)
- Supporting check: mean unusual 3-bar move of grid bars with forecast > 0: 0.00439372, passed: True
- Counts: grid bars with forecast > 0: 299, grid bars in total: 478
- Decided by: Minimum count not reached: 299 grid bars with forecast > 0 (minimum 300) and 478 grid bars in total (minimum 1000).
- Reading: The coin's mean 3-bar return is taken on the same non-overlapping grid pooled over all its windows, grid bars without a full 3-bar forward return in their window are dropped, the slope t is the ordinary OLS t on the pooled grid, and the plan's 'inconclusive with too few bars' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.66 % per case over 3 bars, 0.023 of the coin's usual move (10.22 %); normal drift in its direction +2.50 %, total +3.16 %; 251 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d.md`
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2016_2017/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d`
Measure: `measure.py`
