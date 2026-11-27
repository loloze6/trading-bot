---
plan: 075-01_heavy-volume-next-day-rise_1d
idea: 075-01_heavy-volume-next-day-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast: 0.000193671; OLS slope t, clustered by day: 3.05409 (threshold: slope t (clustered by day) >= 2 with supporting check passing confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: top-fifth minus bottom-fifth mean next-day excess return: 0.00588586, passed: True
- Counts: distinct days with recorded forecasts: 2922, bars in slope: 36948, day clusters: 2898
- Decided by: The slope's t is 2 or more and the top-minus-bottom-fifth excess return is above 0.
- Reading: Every bar with a forecast and a same-window next close enters (zero forecasts included); the slope's t uses an intercept and CR1 cluster-robust errors by UTC day; top/bottom fifths are forecast >= pooled 80th / <= pooled 20th percentile; 'days with recorded forecasts' are distinct UTC days with a non-missing forecast on any coin.
- Size: unusual move +0.09 % (t 1.30, the cases of one day together: 2832 days) per case over 1 bars, 0.014 of the coin's usual move (5.31 %); normal drift in its direction -0.03 %, total +0.07 %; 18657 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001347 on the check folds against +0.0001937 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/075-01_heavy-volume-next-day-rise_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01_heavy-volume-next-day-rise_1d`
Measure: `measure.py`
