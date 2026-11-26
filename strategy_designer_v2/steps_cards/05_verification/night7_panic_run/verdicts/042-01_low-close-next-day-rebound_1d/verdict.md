---
plan: 042-01_low-close-next-day-rebound_1d
idea: 042-01_low-close-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of drift-removed next-day return on forecast: 0.000604317; t, day-clustered SE: 2.6437 (threshold: slope t >= 2 confirms (with top-minus-bottom > 0), t <= -2 rejects)
- Supporting check: top minus bottom forecast quintile drift-removed next-day return: 0.00499561, passed: True
- Counts: distinct days with recorded forecasts: 2898, observations: 17380, top quintile observations: 3476, bottom quintile observations: 3476
- Decided by: The slope's t is 2 or more and the top-minus-bottom quintile difference is above 0.
- Reading: The situation is the standardised close location above (long) or below (short) its usual size of +10, rebuilt from last_history_value with a full 60-bar in-window history and otherwise read from post_pipeline_value; the horizon of 1 bar uses every bar; quintiles are pooled over all coins and windows by forecast rank; the 1000-day count is the distinct UTC days in the slope's sample; the slope has an intercept and cluster-robust (CR1) day-clustered errors.
- Size: unusual move +0.22 % (t 2.46, the cases of one day together: 2539 days) per case over 1 bars, 0.049 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.22 %; 7862 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001024 on the check folds against +0.0006043 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/042-01_low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/042-01_low-close-next-day-rebound_1d`
Measure: `measure.py`
