---
plan: 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d
idea: 031-02.b1.b1.b1.g1_wide-day-extends-up-run
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 3-bar forward return on forecast (regime bars, 3-bar grid): 0.00119279; t of slope, day-clustered: 2.44252 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean drift-adjusted 3-bar return, top third minus bottom third of forecasts: 0.0112147, passed: True
- Counts: regime grid cases: 6105, days: 851
- Decided by: The slope is above 0 with t >= 2 and the top-minus-bottom-third check is above 0.
- Reading: Situation check uses close[t]/close[t-6]-1 > 0 inside each window, leaving out active bars of a window's first 6 rows where it cannot be computed; regime bars are rows with regime == 'trending'; the coin's normal 3-bar drift is its mean 3-bar return over the non-overlapping grid (positions 0,3,6,...) of all its windows; the slope is OLS of drift-adjusted return on forecast with a day-clustered standard error (CR1 G/(G-1) scaling, days by UTC date); top and bottom thirds are the n//3 highest and lowest forecasts by rank (ties broken by coin, window, time); the plan's 'fewer than 300 cases' rule is reported as 'not observable'.
- Size: unusual move +0.16 % (t 0.75, the cases of one day together: 1841 days) per case over 3 bars, 0.016 of the coin's usual move (9.14 %); normal drift in its direction +0.48 %, total +0.63 %; 6658 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d`
Measure: `measure.py`
