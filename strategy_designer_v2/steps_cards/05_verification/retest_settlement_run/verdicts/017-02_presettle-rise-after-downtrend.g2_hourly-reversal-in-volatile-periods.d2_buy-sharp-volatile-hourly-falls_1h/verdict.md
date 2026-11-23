---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 24-bar excess return (minus the coin's normal drift) of the bets: -0.000127754; t of the mean: -0.324393 (threshold: t >= 2 with at least 30 cases to confirm; t <= -2 with at least 30 cases to reject)
- Supporting check: mean excess above median entry forecast minus below: 0.000982674, passed: True
- Counts: cases: 16662, cases above median: 8331, cases at or below median: 8331
- Decided by: The main t lies between -2 and 2.
- Reading: Situation bars are those whose raw scaled_fall value (or, where unrecorded, the hour's price return) is below 0 with a positive forecast; a bet is a forecast rise of at least 2 points above its lowest positive level since the last bet (from 0 after a flat), the first bet in each 24-bar grid cell from the window's first row counts, the drift is the coin's mean 24-bar return on that grid over all its windows, and the median split puts cases strictly above the median entry forecast against those at or below it.
- Size: unusual move -0.01 % per case over 24 bars, -0.004 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.13 %; 16662 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h`
Measure: `measure.py`
