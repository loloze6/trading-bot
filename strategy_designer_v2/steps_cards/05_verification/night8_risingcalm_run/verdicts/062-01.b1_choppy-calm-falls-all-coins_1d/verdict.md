---
plan: 062-01.b1_choppy-calm-falls-all-coins_1d
idea: 062-01.b1_choppy-calm-falls-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of next 5-bar excess return on forecast (forecast < 0, 5-bar grid, days pooled): 0.000644946; OLS slope t, day-clustered: 0.867843 (threshold: confirm if t >= 2 and mean short unusual move > 0; reject if t <= -2; minimum 30 cases on 20 distinct days)
- Supporting check: mean unusual move in the short direction: 0.00269677, passed: True
- Counts: grid bars with forecast below 0: 500, distinct days: 208
- Decided by: The slope's t is between -2 and 2.
- Reading: Profile read from the recorded regime ('unknown' = choppy calm); grid = positions 0,5,10,... of each window with a full 5-bar forward return inside the window; normal drift = coin's mean 5-bar return on that grid over all its windows; 'cases of one day pooled' = OLS slope with standard errors clustered by UTC day (CR1); supporting mean = plain mean over cases; the plan's minimum counts are applied as 'not observable'.
- Size: unusual move +0.32 % (t 0.75, the cases of one day together: 530 days) per case over 5 bars, 0.030 of the coin's usual move (11.68 %); normal drift in its direction -0.69 %, total -0.38 %; 916 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/062-01.b1_choppy-calm-falls-all-coins_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/062-01.b1_choppy-calm-falls-all-coins_1d`
Measure: `measure.py`
