---
plan: 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d
idea: 031-02.b1.b1.b1.g1_wide-day-extends-up-run
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 3-bar forward return on forecast (regime bars, 3-bar grid): 0.000802292; t of slope, day-clustered: 0.643646 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean drift-adjusted 3-bar return, top third minus bottom third of forecasts: 0.00954671, passed: True
- Counts: regime grid cases: 882, days: 97
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation check uses close[t]/close[t-6]-1 > 0 inside each window, leaving out active bars of a window's first 6 rows where it cannot be computed; regime bars are rows with regime == 'trending'; the coin's normal 3-bar drift is its mean 3-bar return over the non-overlapping grid (positions 0,3,6,...) of all its windows; the slope is OLS of drift-adjusted return on forecast with a day-clustered standard error (CR1 G/(G-1) scaling, days by UTC date); top and bottom thirds are the n//3 highest and lowest forecasts by rank (ties broken by coin, window, time); the plan's 'fewer than 300 cases' rule is reported as 'not observable'.
- Size: unusual move +0.36 % (t 0.72, the cases of one day together: 228 days) per case over 3 bars, 0.054 of the coin's usual move (6.81 %); normal drift in its direction +0.02 %, total +0.39 %; 1005 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d`
Measure: `measure.py`
