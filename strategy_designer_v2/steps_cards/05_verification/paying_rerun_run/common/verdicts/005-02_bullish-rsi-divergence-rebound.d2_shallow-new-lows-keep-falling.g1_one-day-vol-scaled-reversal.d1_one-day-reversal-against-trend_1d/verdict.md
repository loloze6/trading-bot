---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of position held x (next-day return - coin mean daily return), forecast != 0 bars: 0.000851213; t of the mean: 4.64745 (threshold: confirm if t >= 2 with top-minus-bottom third > 0; reject if t <= -2; else inconclusive; at least 100 cases)
- Supporting check: top-minus-bottom third of |forecast|, drift-adjusted directional next-day return: 0.000566319, passed: True
- Counts: cases: 24384
- Decided by: The main measure's t is 2 or more and the top-minus-bottom third difference is above 0.
- Reading: Position held is postRebalance_current_allocation; the directional return for the thirds is sign(forecast) x drift-adjusted next-day return; thirds are equal-count splits of cases ranked by |forecast| (ties by order); the pool of fewer than 100 cases is treated as the plan's minimum count; the 50-day side is recomputed within a window where 50 bars exist, otherwise read from the recorded regime.
- Size: unusual move +0.24 % (t 2.40, the cases of one day together: 3117 days) per case over 1 bars, 0.044 of the coin's usual move (5.44 %); normal drift in its direction +0.00 %, total +0.24 %; 16667 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d`
Measure: `measure.py`
