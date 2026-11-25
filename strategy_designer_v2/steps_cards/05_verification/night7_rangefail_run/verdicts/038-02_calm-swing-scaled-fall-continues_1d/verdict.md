---
plan: 038-02_calm-swing-scaled-fall-continues_1d
idea: 038-02_calm-swing-scaled-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward excess return on forecast (grid bars with forecast < 0): 0.000843771; slope t, same-day cases summed (day-clustered): 1.47616 (threshold: slope > 0 with t >= 2 confirms (with supporting check > 0); slope < 0 with t <= -2 rejects)
- Supporting check: mean short-side excess return on grid bars with forecast <= -2: 2.29799e-05, passed: True
- Counts: grid cases with forecast < 0: 1654, grid cases with forecast <= -2: 1433, days of the forecast < 0 cases: 359
- Decided by: The slope's t lies between -2 and 2.
- Reading: Grid cases are bars at positions 0,5,10,... of each window with a 5-bar forward return inside the window; the coin's mean 5-bar return is the mean over all its grid returns in all windows; the slope's t sums the regression scores per calendar day (day-clustered SE); the situation is regime not 'chop' with raw value < 0, short.
- Size: unusual move +0.38 % (t 1.05, the cases of one day together: 904 days) per case over 5 bars, 0.034 of the coin's usual move (11.68 %); normal drift in its direction -0.69 %, total -0.32 %; 2267 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/038-02_calm-swing-scaled-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/038-02_calm-swing-scaled-fall-continues_1d`
Measure: `measure.py`
