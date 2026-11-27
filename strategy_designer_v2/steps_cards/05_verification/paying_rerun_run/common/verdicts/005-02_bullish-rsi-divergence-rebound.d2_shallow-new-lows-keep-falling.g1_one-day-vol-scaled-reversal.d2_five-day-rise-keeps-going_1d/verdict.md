---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the demeaned 3-bar forward return on the forecast (non-overlapping grid, pooled): 6.02146; OLS slope t: 6.02146 (threshold: confirm if slope t >= 2 with a positive supporting check; reject if slope t <= -2)
- Supporting check: mean unusual 3-bar move of grid bars with forecast > 0: 0.002254, passed: True
- Counts: grid bars with forecast > 0: 9076, grid bars in total: 18359
- Decided by: Confirm rule met: slope t >= 2 and the mean unusual move of forecast > 0 grid bars is above 0.
- Reading: The coin's mean 3-bar return is taken on the same non-overlapping grid pooled over all its windows, grid bars without a full 3-bar forward return in their window are dropped, the slope t is the ordinary OLS t on the pooled grid, and the plan's 'inconclusive with too few bars' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.17 % (t 0.81, the cases of one day together: 2091 days) per case over 3 bars, 0.018 of the coin's usual move (9.27 %); normal drift in its direction +0.45 %, total +0.63 %; 8584 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d`
Measure: `measure.py`
