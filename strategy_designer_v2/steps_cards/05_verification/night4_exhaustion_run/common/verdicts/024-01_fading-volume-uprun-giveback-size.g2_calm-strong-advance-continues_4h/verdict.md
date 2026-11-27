---
plan: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h
idea: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-18-bar return minus coin's mean 18-bar return, on the forecast: 0.00072059; OLS t of the slope: 5.0311 (threshold: confirm: slope > 0 with t >= 2 and low-vol slope > high-vol slope; reject: slope < 0 with t <= -2)
- Supporting check: low-vol slope minus high-vol slope: -0.000172462, passed: False
- Counts: grid cases with a forecast above 0: 5672, low-volatility grid cases with a forecast above 0: 2142, high-volatility grid cases with a forecast above 0: 2140, grid cases in the regression: 11111
- Decided by: the main t is >= 2 but the low-volatility slope does not exceed the high-volatility slope.
- Reading: all grid bars (positions 0, 18, 36, ... of each window with a full 18-bar forward return), forecast 0 included, enter the regressions; the coin's mean is the mean of its grid 18-bar returns over all windows; volatility is the rolling 180-bar std of 4h close returns inside each window (grid cases without 180 past returns are left out of the split), split at the coin's median over its grid cases with low = at or below the median; the minimum counts are counted on grid cases with a forecast above 0.
- Size: unusual move -0.05 % (t -0.29, the cases of one day together: 2210 days) per case over 18 bars, -0.004 of the coin's usual move (9.37 %); normal drift in its direction +0.71 %, total +0.65 %; 8609 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h`
Measure: `measure.py`
