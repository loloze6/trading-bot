---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of forecast/10 x 24-bar excess return (non-overlapping grid, pooled): 0.00263806; t of the mean: 5.66719 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean sign(forecast) x excess return, largest |forecast| third minus smallest third: 0.00340665, passed: True
- Counts: cases with a non-zero forecast: 17147, cases in largest third: 5715, cases in smallest third: 5716
- Decided by: The mean product is positive with t >= 2 and the largest-third minus smallest-third difference is > 0 (confirm rule).
- Reading: Cases are grid bars (positions 0, 24, 48, ... of each window) with a non-zero forecast and a 24-bar forward return inside the window; the coin's normal drift is the mean of all its grid 24-bar returns over all windows; thirds are formed by sorting cases on |forecast| (stable sort) and splitting into three near-equal groups; the plan's 500-case minimum, when not met, gives 'not observable'.
- Size: unusual move +0.08 % per case over 24 bars, 0.015 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.08 %; 17246 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h`
Measure: `measure.py`
