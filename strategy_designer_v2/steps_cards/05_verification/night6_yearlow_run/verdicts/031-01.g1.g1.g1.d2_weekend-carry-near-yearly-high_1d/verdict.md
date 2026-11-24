---
plan: 031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high_1d
idea: 031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess weekend return on forecast (post_pipeline_value): 0.000451213; slope t, deviations summed per day (day-clustered): 0.987292 (threshold: confirm at t >= 2 (with weighted mean excess > 0), reject at t <= -2)
- Supporting check: forecast-weighted mean excess weekend return > 0: 0.00977309, passed: True
- Counts: cases: 1192, distinct Fridays: 317
- Decided by: Inconclusive: the slope t lies between -2 and 2.
- Reading: Friday = timestamp (bar start, UTC) weekday 4 and the 14-bar return is close[t]/close[t-14]-1 inside the window; active bars in a window's first 14 rows, where it cannot be computed, are left out of the agreement; a case is a Friday bar with regime 'trending', a recorded post_pipeline_value and close[t+2] in the same window; 'deviations summed per day' is read as a day-clustered standard error of the slope (slope-score terms (x-mean x)*residual summed per day, factor G/(G-1)); a missing minimum count gives 'not observable' as the workflow requires.
- Size: unusual move +0.85 % (t 3.27, the cases of one day together: 315 days) per case over 2 bars, 0.127 of the coin's usual move (6.58 %); normal drift in its direction +0.26 %, total +1.11 %; 1164 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high_1d`
Measure: `measure.py`
