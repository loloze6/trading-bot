---
plan: 031-02.b2.a1.b2_deep-fall-rebound-45-days_1d
idea: 031-02.b2.a1.b2_deep-fall-rebound-45-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 45-day return on forecast, non-overlapping grid cases, all coins: 0.00159424; slope t, same-day cases clustered: 0.363877 (threshold: confirm if slope t >= 2 and supporting check passes; reject if slope t <= -2; else inconclusive)
- Supporting check: forecast-weighted mean excess 45-day return over grid cases with forecast > 0, above 0: 0.0139526, passed: True
- Counts: grid cases: 488, grid cases with forecast > 0: 265, distinct days of grid cases with forecast > 0: 37, distinct days of all grid cases: 50
- Decided by: Inconclusive rule: the slope t lies between -2 and 2.
- Reading: Situation = raw fall90 value below zero with forecast > 0 (bars with the raw value missing count as not agreeing); grid = positions 0, 45, 90, ... of each window with t+45 inside the window; the coin's mean 45-day return is the mean over all its grid returns in all its windows; the slope is a one-variable OLS with intercept over all grid cases (forecast 0 included) and its t uses a day-clustered standard error (cross-products summed per UTC day, G/(G-1) correction); the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow.
- Size: unusual move +0.80 % (t 0.22, the cases of one day together: 153 days) per case over 45 bars, 0.008 of the coin's usual move (36.02 %); normal drift in its direction +10.25 %, total +11.05 %; 319 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b2.a1.b2_deep-fall-rebound-45-days_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b2.a1.b2_deep-fall-rebound-45-days_1d`
Measure: `measure.py`
