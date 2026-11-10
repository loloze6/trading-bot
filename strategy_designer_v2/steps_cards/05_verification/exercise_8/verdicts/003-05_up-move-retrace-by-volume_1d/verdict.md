---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted next-bar return, heavy minus thin up bars: -0.000663565; Welch t: -0.151697 (threshold: confirm if difference > 0 and t >= 2; reject if difference < 0 and t <= -2; otherwise inconclusive)
- Supporting check: weighted thin-up next-bar return minus unconditional mean daily return: 0.00104926, passed: False
- Counts: heavy_up_bars: 151, thin_up_bars: 194
- Decided by: The t-statistic lies between -2 and 2, so the test is inconclusive.
- Reading: Heavy versus thin is the bar's volume at or above its 20-bar rolling mean including the bar, computed inside each window (bars without 20 bars of volume history are checked only for being up bars); in the measure, the groups are forecast-bearing up bars split by forecast sign (long = heavy, short = thin), weighted by |forecast|, and the Welch t uses weighted variances with Kish effective sample sizes; the unconditional mean is the plain mean of all next-bar returns in the windows.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
