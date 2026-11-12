---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean next-bar return, heavy up bars minus thin up bars: -0.000663565; Welch t (weighted): -0.151697 (threshold: confirm if difference > 0 and t >= 2; reject if difference < 0 and t <= -2)
- Supporting check: thin-up weighted mean next-bar return minus unconditional mean daily return (< 0): 0.00104926, passed: False
- Counts: heavy forecast-bearing up bars: 151, thin forecast-bearing up bars: 194
- Decided by: The t-statistic lies between -2 and 2.
- Reading: Up bar = one-bar move (heavy_up/thin_up last_history_value) > 0; heavy/thin groups are the forecast-bearing up bars with positive/negative forecast; the Welch t uses |forecast|-weighted means and variances with Kish effective sample sizes; the unconditional mean is the plain mean of all next-bar returns in all windows; the plan's 30-bar minimum per group is applied as 'not observable'; in the situation check, active up bars in the first 19 rows of a window (20-bar volume mean not computable) count as on-side.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
