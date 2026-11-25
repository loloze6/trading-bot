---
plan: 045-01_agitated-wide-low-close-rebound_1d
idea: 045-01_agitated-wide-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day demeaned return on forecast (post_pipeline_value): -0.000170571; slope t, day-clustered: -0.347074 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 cases over at least 150 distinct days)
- Supporting check: none
- Counts: cases: 953, distinct days: 459
- Decided by: Inconclusive rule: t lies between -2 and 2.
- Reading: Situation bars are non-chop regime bars with a positive raw close-below-high value and a positive forecast; the regression has an intercept, and its t uses a day-clustered standard error (residual x centred forecast summed per UTC day) with the G/(G-1) correction, on every bar since the 1-bar grid is every bar.
- Size: unusual move -0.65 % (t -1.76, the cases of one day together: 246 days) per case over 1 bars, -0.094 of the coin's usual move (6.78 %); normal drift in its direction +0.84 %, total +0.19 %; 368 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/045-01_agitated-wide-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/045-01_agitated-wide-low-close-rebound_1d`
Measure: `measure.py`
