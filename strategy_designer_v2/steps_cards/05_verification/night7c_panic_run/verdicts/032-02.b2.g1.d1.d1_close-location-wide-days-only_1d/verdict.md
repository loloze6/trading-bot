---
plan: 032-02.b2.g1.d1.d1_close-location-wide-days-only_1d
idea: 032-02.b2.g1.d1.d1_close-location-wide-days-only
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-day excess return on post_pipeline_value, mean_reversion bars: 0.000237078; day-clustered t of the slope: 3.30672 (threshold: confirm: slope > 0 with day-clustered t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2 or supporting mean < 0 with t <= -2; at least 300 distinct days with regime bars)
- Supporting check: mean of sign(forecast) x next-day excess return, top third by |forecast|: 0.00572418, passed: True
- Counts: distinct days with regime bars: 2126, regime bars in the slope: 6674, bars in the top third: 2224
- Decided by: Confirm: the slope is positive with t = 3.31 >= 2 and the supporting check's mean is above 0.
- Reading: Width is recomputed per window as range > mean range of the previous 20 bars (from prices, or from last_history_value where the window has under 20 prior bars); the slope is OLS with intercept and day-clustered standard error (scores summed per UTC day, G/(G-1) correction); the supporting check uses the floor(n/3) regime bars with the largest |forecast| and a day-clustered t of the mean; the day count is the distinct UTC days of regime bars with a valid forecast value and next-day return.
- Size: unusual move +0.33 % (t 2.99, the cases of one day together: 1962 days) per case over 1 bars, 0.069 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.33 %; 5396 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +9.741e-05 on the check folds against +0.0002371 on every fold
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g1.d1.d1_close-location-wide-days-only_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d1.d1_close-location-wide-days-only_1d`
Measure: `measure.py`
