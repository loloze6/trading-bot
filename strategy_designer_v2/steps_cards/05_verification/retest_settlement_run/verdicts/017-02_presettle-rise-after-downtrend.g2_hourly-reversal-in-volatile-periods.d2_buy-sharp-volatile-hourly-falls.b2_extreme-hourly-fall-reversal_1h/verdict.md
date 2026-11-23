---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 24-bar move of the cases (return minus coin's normal 24-bar drift, long): 0.000199576; t of the mean: 0.514565 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: upper-half minus lower-half mean unusual move (median split of forecast): -0.000552109, passed: False
- Counts: cases: 17184
- Decided by: t between -2 and 2 over at least 30 cases.
- Reading: A bet is a rise of the forecast of >= 2 points above its lowest positive level since the last bet (reset to 0 when the forecast is not positive), the first bet in each 24-bar grid cell (from each window's first row) is the case, cases without 24 bars left in the window are dropped, the normal drift is the coin's mean non-overlapping 24-bar return over all its windows, and the median split sorts the cases by forecast (stable, in coin/window/time order) and puts the first floor(n/2) in the lower half.
- Size: unusual move +0.02 % per case over 24 bars, 0.003 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.16 %; 17184 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h`
Measure: `measure.py`
