---
plan: 031-03.g1.b1.d2.e2.d1_volume-swell-long-only_1d
idea: 031-03.g1.b1.d2.e2.d1_volume-swell-long-only
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 14-bar excess return on positive-forecast grid bars: 0.0260922; t of the weighted mean, cases of one day summed: 1.42865 (threshold: confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of excess 14-bar return on forecast: 0.0018014, passed: True
- Counts: positive-forecast grid cases: 1145, distinct days: 182
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The normal drift is each coin's mean 14-bar return on the non-overlapping grid of all its windows, and the day-clustered t sums the weighted deviations f*(x-mean) per UTC day with a D/(D-1) correction, the standard error being divided by the sum of forecasts.
- Size: unusual move +1.57 % (t 1.73, the cases of one day together: 807 days) per case over 14 bars, 0.063 of the coin's usual move (20.98 %); normal drift in its direction +2.49 %, total +4.06 %; 1415 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.d1_volume-swell-long-only_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.d1_volume-swell-long-only_1d`
Measure: `measure.py`
