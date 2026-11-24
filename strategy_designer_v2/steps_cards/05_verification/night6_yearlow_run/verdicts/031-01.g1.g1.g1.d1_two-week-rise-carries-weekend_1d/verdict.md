---
plan: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d
idea: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered OLS slope of excess 2-bar return on forecast (Friday-close, forecast > 0): 0.00043925; slope t, clustered by day: 1.29301 (threshold: slope t >= 2 confirms (with weighted mean excess > 0); slope t <= -2 rejects)
- Supporting check: forecast-weighted mean excess 2-bar return > 0: 0.0107246, passed: True
- Counts: cases with forecast > 0: 1215, distinct Fridays: 319
- Decided by: The slope's t lies between -2 and 2.
- Reading: Friday-close bars are the daily bars opening on Friday UTC (next bar Saturday); all such bars with forecast > 0 in the trending regime are used (weekly cases never overlap), the coin's mean 2-bar return is taken on each window's non-overlapping 0,2,4,... grid pooled over windows, the slope t uses CR1 standard errors clustered by date, and the plan's minimum counts not reached give 'not observable'.
- Size: unusual move +0.92 % (t 3.37, the cases of one day together: 291 days) per case over 2 bars, 0.136 of the coin's usual move (6.58 %); normal drift in its direction +0.23 %, total +1.16 %; 1065 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d`
Measure: `measure.py`
