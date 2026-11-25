---
plan: 032-02.g1.e1_raw-nearness-to-uptrend-high_1d
idea: 032-02.g1.e1_raw-nearness-to-uptrend-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the OLS slope of excess 5-bar return on forecast (grid bars, forecast > 0): 0.000675807; t of OLS slope: 1.65271 (threshold: confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2)
- Supporting check: forecast-weighted mean excess 5-bar return > 0: 0.00559098, passed: True
- Counts: grid cases with forecast > 0: 1700
- Decided by: The slope's t is 1.65, between -2 and 2.
- Reading: The situation is close above the close 28 bars before, recomputed from the window's prices, using the recorded regime on the first 28 bars of a window where that close is not recorded, with a recorded proximity in (0, 1] and a long forecast. The coin's mean 5-bar return is taken over the non-overlapping grid (positions 0, 5, 10, ...) of all its windows. Grid bars without a full 5-bar forward return inside their window are left out. The plan's fewer-than-100-cases rule is applied as the minimum count, giving 'not observable'.
- Size: unusual move +0.78 % (t 1.88, the cases of one day together: 836 days) per case over 5 bars, 0.064 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +1.36 %; 1449 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e1_raw-nearness-to-uptrend-high_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1_raw-nearness-to-uptrend-high_1d`
Measure: `measure.py`
