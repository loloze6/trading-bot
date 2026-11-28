---
plan: 089-02_calm-decline-up-down-volume-ratio_1d
idea: 089-02_calm-decline-up-down-volume-ratio
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 5-bar excess return (forecast > 0, non-overlapping grid): -0.00650193; t of the weighted mean, clustered by day: -0.939143 (threshold: confirm: above 0 with t >= 2 (and Spearman > 0); reject: below 0 with t <= -2)
- Supporting check: Spearman correlation forecast vs 5-bar excess return: 0.0375289, passed: True
- Counts: cases with forecast > 0: 347, distinct days: 203
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive. No effect (common/verdicts.md): t in the idea's direction -0.939 (below 1), 347 cases (30 needed).
- Reading: The falling calm profile is read from the recorded regime ('unknown' = neither veto fired, since the 365-bar volatility percentile cannot be rebuilt from the windows' bars) and the lean from the raw log ratio being above 0 with a long forecast; the coin's mean 5-bar return is the mean over all its non-overlapping grid returns of all its windows; the clustered t uses the weighted-mean deviations summed per UTC day with a G/(G-1) correction; the plan's minimum counts lead to 'not observable' as the workflow requires.
- Size: unusual move -0.56 % (t -1.04, the cases of one day together: 338 days) per case over 5 bars, -0.048 of the coin's usual move (11.31 %); normal drift in its direction +0.64 %, total +0.08 %; 403 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.939 (below 1), 347 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/089-02_calm-decline-up-down-volume-ratio_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/089-02_calm-decline-up-down-volume-ratio_1d`
Measure: `measure.py`
