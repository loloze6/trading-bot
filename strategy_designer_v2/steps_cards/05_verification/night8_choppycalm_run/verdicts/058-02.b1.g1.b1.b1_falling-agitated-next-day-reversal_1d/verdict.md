---
plan: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d
idea: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on post_pipeline forecast (day-clustered t): 0.00052853; day-clustered OLS t: 3.22608 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return in forecast direction, top fifth of |forecast|: 0.00717057, passed: True
- Counts: non-zero-forecast bars: 5410, distinct days: 1269
- Decided by: The slope is positive with t >= 2 and the supporting check passes.
- Reading: Situation bars are active bars whose raw scaled move (last_history_value, recomputed from prices if missing) is non-zero with the forecast of the opposite sign; the excess return subtracts the coin's mean 1-bar return over all its windows; the t uses day-clustered standard errors with a G/(G-1) correction; the top fifth is |forecast| at or above the 80th percentile of the regression cases; the plan's minimum counts are applied to the regression cases and, per instructions, give 'not observable' when not met.
- Size: unusual move +0.60 % (t 3.19, the cases of one day together: 1049 days) per case over 1 bars, 0.124 of the coin's usual move (5.33 %); normal drift in its direction +0.01 %, total +0.61 %; 3578 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003734 on the check folds against +0.0005285 on every fold
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d`
Measure: `measure.py`
