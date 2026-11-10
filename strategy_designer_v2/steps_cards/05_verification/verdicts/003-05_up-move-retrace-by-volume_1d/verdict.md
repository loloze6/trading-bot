---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Situation check: 0.982759 of the active bars match the plan's situation and side
Evidence:
- Main measure: heavy-minus-thin |forecast|-weighted mean next-bar return: -0.000663565; Welch t: -0.151697 (threshold: Confirm if difference > 0 and t >= 2; reject if difference < 0 and t <= -2; else inconclusive; inconclusive if fewer than 30 up bars in either group)
- Supporting check: thin weighted mean next-bar return minus unconditional mean daily return (< 0): 0.00104926, passed: False
- Counts: heavy up bars: 151, thin up bars: 194
- Decided by: Inconclusive: t lies between -2 and 2.
- Reading: Volume's 20-bar mean is a within-window rolling mean including the current bar (min_periods=1, since warm-up bars are absent); heavy and thin groups are the forecast-bearing up bars with long and short forecast respectively; the Welch t uses |forecast|-weighted means and weighted variances with Kish effective sample sizes; the unconditional mean is the plain mean of all next-bar returns pooled over the windows.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
