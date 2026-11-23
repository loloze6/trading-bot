---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 24-bar excess return over coin's mean 24-bar return, per bet case: 0.00088762; t of the mean: 1.58417 (threshold: confirm: mean > 0 with t >= 2 (and larger-forecast half beats smaller); reject: mean < 0 with t <= -2)
- Supporting check: mean excess of above-median-forecast half minus at-or-below-median half: None, passed: False
- Counts: independent cases: 9538
- Decided by: The t-statistic lies between -2 and 2.
- Reading: Cases are long-side forecast rises of at least 2 points from the lowest long level since the last bet (reset to 0 on flat), the first such bet in each 24-row grid cell of a window with a full 24 bars ahead; the coin mean is over non-overlapping 24-bar grid returns of all its windows; the median split puts forecasts strictly above the median in the larger half; the plan's 'fewer than 100 cases' is reported as not observable as the workflow requires.
- Size: unusual move +0.09 % per case over 24 bars, 0.015 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.23 %; 9538 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h`
Measure: `measure.py`
