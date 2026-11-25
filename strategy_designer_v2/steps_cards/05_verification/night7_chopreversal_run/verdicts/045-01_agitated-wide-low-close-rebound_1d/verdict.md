---
plan: 045-01_agitated-wide-low-close-rebound_1d
idea: 045-01_agitated-wide-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day demeaned return on forecast (post_pipeline_value): 0.000669906; slope t, day-clustered: 3.83464 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 cases over at least 150 distinct days)
- Supporting check: none
- Counts: cases: 7650, distinct days: 2211
- Decided by: Confirm rule: slope positive with t >= 2 on at least 300 cases over at least 150 distinct days.
- Reading: Situation bars are non-chop regime bars with a positive raw close-below-high value and a positive forecast; the regression has an intercept, and its t uses a day-clustered standard error (residual x centred forecast summed per UTC day) with the G/(G-1) correction, on every bar since the 1-bar grid is every bar.
- Size: unusual move +0.27 % (t 1.58, the cases of one day together: 1325 days) per case over 1 bars, 0.061 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.40 %; 3098 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003445 on the check folds against +0.0006699 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/045-01_agitated-wide-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/045-01_agitated-wide-low-close-rebound_1d`
Measure: `measure.py`
