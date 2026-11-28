---
plan: 050-02.b2_calm-downtrend-week-rise-five-days_1d
idea: 050-02.b2_calm-downtrend-week-rise-five-days
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return over holding the coin, cases forecast > 0: -0.00162456; t of the mean, cases of one day taken together: -0.209075 (threshold: confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: t <= -2)
- Supporting check: OLS slope of excess 5-bar return on forecast: -0.000804861, passed: False
- Counts: cases: 264, distinct days: 146
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive. No effect (common/verdicts.md): t in the idea's direction -0.209 (below 1), 264 cases (30 needed).
- Reading: Cases are grid bars (positions 0,5,10,... per window with a full 5-bar forward return) with forecast > 0; the coin's mean is over all its windows' grid 5-bar returns; the profile is the recorded regime 'unknown'; the plan's 'fewer cases' rule is applied as 'not observable' as the workflow requires.
- Size: unusual move +0.49 % (t 0.95, the cases of one day together: 299 days) per case over 5 bars, 0.047 of the coin's usual move (11.31 %); normal drift in its direction +0.60 %, total +1.09 %; 427 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.209 (below 1), 264 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-02.b2_calm-downtrend-week-rise-five-days_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b2_calm-downtrend-week-rise-five-days_1d`
Measure: `measure.py`
