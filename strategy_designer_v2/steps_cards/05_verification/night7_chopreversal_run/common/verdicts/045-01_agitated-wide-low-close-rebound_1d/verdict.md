---
plan: 045-01_agitated-wide-low-close-rebound_1d
idea: 045-01_agitated-wide-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day demeaned return on forecast (post_pipeline_value): 0.000492664; slope t, day-clustered: 3.07818 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 cases over at least 150 distinct days)
- Supporting check: none
- Counts: cases: 19581, distinct days: 3143
- Decided by: Confirm rule: slope positive with t >= 2 on at least 300 cases over at least 150 distinct days.
- Reading: Situation bars are non-chop regime bars with a positive raw close-below-high value and a positive forecast; the regression has an intercept, and its t uses a day-clustered standard error (residual x centred forecast summed per UTC day) with the G/(G-1) correction, on every bar since the 1-bar grid is every bar.
- Size: unusual move +0.06 % (t 0.41, the cases of one day together: 2080 days) per case over 1 bars, 0.012 of the coin's usual move (5.12 %); normal drift in its direction +0.12 %, total +0.18 %; 7918 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/045-01_agitated-wide-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/common/backtests/045-01_agitated-wide-low-close-rebound_1d`
Measure: `measure.py`
