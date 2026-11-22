---
plan: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h
idea: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-18-bar return minus coin's mean 18-bar return, on the forecast: 0.000686052; OLS t of the slope: 4.09448 (threshold: confirm: slope > 0 with t >= 2 and low-vol slope > high-vol slope; reject: slope < 0 with t <= -2)
- Supporting check: low-vol slope minus high-vol slope: 0.000589527, passed: True
- Counts: grid cases with a forecast above 0: 2916, low-volatility grid cases with a forecast above 0: 1112, high-volatility grid cases with a forecast above 0: 1092, grid cases in the regression: 5724
- Decided by: the main slope is positive with t >= 2 and the low-volatility slope exceeds the high-volatility slope.
- Reading: all grid bars (positions 0, 18, 36, ... of each window with a full 18-bar forward return), forecast 0 included, enter the regressions; the coin's mean is the mean of its grid 18-bar returns over all windows; volatility is the rolling 180-bar std of 4h close returns inside each window (grid cases without 180 past returns are left out of the split), split at the coin's median over its grid cases with low = at or below the median; the minimum counts are counted on grid cases with a forecast above 0.
- Size: unusual move -0.03 % per case over 18 bars, -0.006 of the coin's usual move (8.17 %); normal drift in its direction +0.40 %, total +0.37 %; 4453 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h`
Measure: `measure.py`
