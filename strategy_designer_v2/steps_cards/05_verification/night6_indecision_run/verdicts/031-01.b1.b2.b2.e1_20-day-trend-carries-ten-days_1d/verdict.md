---
plan: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d
idea: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward return minus coin's normal 10-bar drift on the forecast: 0.00132756; OLS slope t: 2.455 (threshold: confirm if t >= 2 (with timing gain > 0); reject if t <= -2)
- Supporting check: book mean daily return minus gain from the market's own rise (timing): 0.000272881, passed: True
- Counts: grid bars with a forecast above 0: 820, grid bars: 1691
- Decided by: The slope has t >= 2 and the timing gain is above 0.
- Reading: The slope is an ordinary least-squares regression over all pooled non-overlapping grid bars (positions 0, 10, 20, ... with a full 10-bar forward return in the window), flat bars with forecast 0 included, with each coin's drift being its mean 10-bar return on that grid over all its windows; the plan's 'else inconclusive' minimum of 100 grid bars with forecast above 0 is applied as 'not observable', as the workflow requires.
- Size: unusual move +0.04 % (t 0.05, the cases of one day together: 540 days) per case over 10 bars, -0.001 of the coin's usual move (14.49 %); normal drift in its direction +1.18 %, total +1.22 %; 981 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d`
Measure: `measure.py`
