---
plan: 059-01_calm-decline-continues-return_1d
idea: 059-01_calm-decline-continues-return
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess forward return on forecast, grid bars with forecast < 0: 0.000495584; OLS t of slope: 0.969911 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2)
- Supporting check: mean unusual move of short cases (>= 2 points) in short direction: 0.00791007, passed: True
- Counts: grid bars with forecast < 0: 907, cases: 959
- Decided by: The slope's t is between -2 and 2.
- Reading: The calm profile is taken as the recorded regime not being 'chop' (the volatility-percentile veto), the coin's mean 5-bar return is the mean of its non-overlapping 5-bar grid returns over all its windows, the regression pools all coins' grid bars with forecast < 0, and the one case per grid cell is the first short bet (rise of at least 2 points in short size from its lowest level since the last bet) in that cell with a full 5-bar forward return.
- Size: unusual move +0.79 % (t 2.02, the cases of one day together: 560 days) per case over 5 bars, 0.078 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total +0.15 %; 959 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/059-01_calm-decline-continues-return_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-01_calm-decline-continues-return_1d`
Measure: `measure.py`
