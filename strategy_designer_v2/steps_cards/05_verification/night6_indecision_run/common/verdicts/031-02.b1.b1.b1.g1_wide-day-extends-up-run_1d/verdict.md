---
plan: 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d
idea: 031-02.b1.b1.b1.g1_wide-day-extends-up-run
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 3-bar forward return on forecast (regime bars, 3-bar grid): 0.00136224; t of slope, day-clustered: 3.0717 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean drift-adjusted 3-bar return, top third minus bottom third of forecasts: 0.0127232, passed: True
- Counts: regime grid cases: 9058, days: 1172
- Decided by: The slope is above 0 with t >= 2 and the top-minus-bottom-third check is above 0.
- Reading: Situation check uses close[t]/close[t-6]-1 > 0 inside each window, leaving out active bars of a window's first 6 rows where it cannot be computed; regime bars are rows with regime == 'trending'; the coin's normal 3-bar drift is its mean 3-bar return over the non-overlapping grid (positions 0,3,6,...) of all its windows; the slope is OLS of drift-adjusted return on forecast with a day-clustered standard error (CR1 G/(G-1) scaling, days by UTC date); top and bottom thirds are the n//3 highest and lowest forecasts by rank (ties broken by coin, window, time); the plan's 'fewer than 300 cases' rule is reported as 'not observable'.
- Size: unusual move +0.28 % (t 1.42, the cases of one day together: 2466 days) per case over 3 bars, 0.027 of the coin's usual move (9.27 %); normal drift in its direction +0.46 %, total +0.73 %; 9864 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d`
Measure: `measure.py`
