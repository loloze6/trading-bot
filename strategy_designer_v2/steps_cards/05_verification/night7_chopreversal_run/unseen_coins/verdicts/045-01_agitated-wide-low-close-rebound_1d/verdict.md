---
plan: 045-01_agitated-wide-low-close-rebound_1d
idea: 045-01_agitated-wide-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day demeaned return on forecast (post_pipeline_value): 0.000519669; slope t, day-clustered: 2.34348 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 cases over at least 150 distinct days)
- Supporting check: none
- Counts: cases: 6799, distinct days: 1644
- Decided by: Confirm rule: slope positive with t >= 2 on at least 300 cases over at least 150 distinct days.
- Reading: Situation bars are non-chop regime bars with a positive raw close-below-high value and a positive forecast; the regression has an intercept, and its t uses a day-clustered standard error (residual x centred forecast summed per UTC day) with the G/(G-1) correction, on every bar since the 1-bar grid is every bar.
- Size: unusual move +0.12 % (t 0.56, the cases of one day together: 1000 days) per case over 1 bars, 0.020 of the coin's usual move (5.40 %); normal drift in its direction +0.15 %, total +0.26 %; 2763 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00031 on the check folds against +0.0005197 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/045-01_agitated-wide-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_coins/backtests/045-01_agitated-wide-low-close-rebound_1d`
Measure: `measure.py`
