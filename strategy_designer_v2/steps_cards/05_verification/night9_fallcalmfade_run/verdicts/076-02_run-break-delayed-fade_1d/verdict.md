---
plan: 076-02_run-break-delayed-fade_1d
idea: 076-02_run-break-delayed-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean excess short return, close t+1 to t+3: 0.000615394; t of the weighted mean, cases of one day taken together: 0.333496 (threshold: confirm: above 0 with t >= 2 (and slope check passes); reject: t <= -2)
- Supporting check: OLS slope of excess short return on run length (t): 1.17306, passed: False
- Counts: cases: 4160, distinct case days: 1429
- Decided by: Neither the confirm rule nor the reject rule is met (inconclusive rule: any other result).
- Reading: A case is the first bar with a negative forecast in each 3-bar grid cell (positions 0,3,6,... of each window) with close[t+3] inside the window; the coin's mean 2-day return uses non-overlapping 2-bar returns pooled over all its windows; the weighted mean's t clusters weighted deviations by UTC day with a D/(D-1) correction; the slope's t is the ordinary unweighted OLS t; and the plan's 'fewer than 300 cases or 200 days' rule is reported as 'not observable'.
- Size: unusual move +0.34 % (t 1.61, the cases of one day together: 1429 days) per case over 3 bars, 0.044 of the coin's usual move (7.96 %); normal drift in its direction -0.36 %, total -0.02 %; 4160 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/076-02_run-break-delayed-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/076-02_run-break-delayed-fade_1d`
Measure: `measure.py`
