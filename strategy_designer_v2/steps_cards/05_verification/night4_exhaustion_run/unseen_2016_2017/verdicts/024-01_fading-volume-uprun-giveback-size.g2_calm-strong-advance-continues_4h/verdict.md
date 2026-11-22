---
plan: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h
idea: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-18-bar return minus coin's mean 18-bar return, on the forecast: 0.00160225; OLS t of the slope: 2.38745 (threshold: confirm: slope > 0 with t >= 2 and low-vol slope > high-vol slope; reject: slope < 0 with t <= -2)
- Supporting check: low-vol slope minus high-vol slope: -0.00139734, passed: False
- Counts: grid cases with a forecast above 0: 517, low-volatility grid cases with a forecast above 0: 196, high-volatility grid cases with a forecast above 0: 196, grid cases in the regression: 893
- Decided by: the main t is >= 2 but the low-volatility slope does not exceed the high-volatility slope.
- Reading: all grid bars (positions 0, 18, 36, ... of each window with a full 18-bar forward return), forecast 0 included, enter the regressions; the coin's mean is the mean of its grid 18-bar returns over all windows; volatility is the rolling 180-bar std of 4h close returns inside each window (grid cases without 180 past returns are left out of the split), split at the coin's median over its grid cases with low = at or below the median; the minimum counts are counted on grid cases with a forecast above 0.
- Size: unusual move -0.01 % per case over 18 bars, 0.003 of the coin's usual move (13.56 %); normal drift in its direction +3.06 %, total +3.05 %; 723 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h`
Measure: `measure.py`
