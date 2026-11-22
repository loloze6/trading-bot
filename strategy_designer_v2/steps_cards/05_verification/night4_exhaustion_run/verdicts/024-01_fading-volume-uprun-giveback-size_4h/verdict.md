---
plan: 024-01_fading-volume-uprun-giveback-size_4h
idea: 024-01_fading-volume-uprun-giveback-size
fit: adapted
status: mismatch
---
Situation check: 26 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the bars with a non-zero forecast are short bars on which the last 4 bars closed up and the mean volume of the last 2 bars is below that of the last 4.
- Reading: Bars whose 4-bar history lies before the window's first recorded bar are left out of the situation check; a case is the first short bet (rise of the short forecast's size of at least 2 points from its lowest size since the last bet, from 0 after a flat or long bar) in each 18-bar grid cell of a window with an 18-bar return inside the window; the drift is the mean 18-bar return on each coin's non-overlapping grid over all its windows; the larger half is the cases with absolute forecast above the median, the smaller half those at or below it.
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size_4h`
Measure: `measure.py`
