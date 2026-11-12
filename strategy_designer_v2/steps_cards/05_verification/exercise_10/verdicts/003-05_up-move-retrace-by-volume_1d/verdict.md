---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: weighted mean next-bar return after heavy up bars minus after thin up bars: -0.000663565; weighted Welch t: -0.151697 (threshold: confirm if difference > 0 with t >= 2; reject if difference < 0 with t <= -2)
- Supporting check: weighted mean next-bar return after thin up bars minus unconditional mean daily return: 0.00104926, passed: False
- Counts: heavy forecast-bearing up bars: 151, thin forecast-bearing up bars: 194
- Decided by: The t-statistic lies between -2 and 2 (inconclusive rule).
- Reading: Heavy/thin up bars are taken as forecast-bearing bars with a positive one-bar move and a positive/negative forecast (the strategy's own volume classification), the volume check uses a 20-bar rolling mean including the current bar (bars without 20 bars of history left out of the agreement), the Welch t uses weighted means, unbiased weighted variances and effective sizes (sum w)^2/sum w^2, the plan's under-30 rule is reported as not observable, and the unconditional mean is the pooled mean of all next-bar returns inside the windows.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
