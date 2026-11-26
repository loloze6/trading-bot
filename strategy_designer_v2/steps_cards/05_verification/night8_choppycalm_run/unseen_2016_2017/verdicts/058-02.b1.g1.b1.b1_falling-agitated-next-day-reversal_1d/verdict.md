---
plan: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d
idea: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on post_pipeline forecast (day-clustered t): 0.000429117; day-clustered OLS t: 0.967821 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return in forecast direction, top fifth of |forecast|: 0.0059136, passed: True
- Counts: non-zero-forecast bars: 36, distinct days: 36
- Decided by: Minimum count not reached: 36 non-zero-forecast bars (< 200) and 36 distinct days (< 60).
- Reading: Situation bars are active bars whose raw scaled move (last_history_value, recomputed from prices if missing) is non-zero with the forecast of the opposite sign; the excess return subtracts the coin's mean 1-bar return over all its windows; the t uses day-clustered standard errors with a G/(G-1) correction; the top fifth is |forecast| at or above the 80th percentile of the regression cases; the plan's minimum counts are applied to the regression cases and, per instructions, give 'not observable' when not met.
- Size: unusual move +0.39 % (t 0.91, the cases of one day together: 24 days) per case over 1 bars, 0.035 of the coin's usual move (6.78 %); normal drift in its direction +0.09 %, total +0.47 %; 24 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d`
Measure: `measure.py`
