---
plan: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed unusual 18-bar move: 0.00557173; t of the mean: 1.74003 (threshold: positive with t >= 2 to confirm; negative with t <= -2 to reject)
- Supporting check: mean unusual move, larger minus smaller absolute forecast (median split): -0.00170385, passed: False
- Counts: cases over all coins and windows: 670, larger-forecast cases: 335, smaller-forecast cases: 335
- Decided by: the t of the mean lies between -2 and 2, which the plan calls inconclusive.
- Reading: the situation is recomputed per window from prices (close below the minimum low of the 12 prior bars and close over the close 180 bars earlier above 1), and active bars whose 180-bar history lies before the window's first recorded row are left out of the agreement; a short bet is a rise of the short forecast's size by at least 2 points from its lowest size since the last bet (from 0 after a flat or a long), the first such bet in each 18-bar grid cell of a window is the cell's case, and cases without 18 bars left in their window are left out; the normal drift is the mean of each coin's 18-bar returns on the 0,18,36,... grid of all its windows; the supporting split puts cases with absolute forecast strictly above the median in the larger group and the rest in the smaller group; the plan's 30-case minimum, when not reached, gives 'not observable'.
- Size: unusual move +0.56 % per case over 18 bars, 0.061 of the coin's usual move (8.17 %); normal drift in its direction -0.41 %, total +0.14 %; 670 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h`
Measure: `measure.py`
