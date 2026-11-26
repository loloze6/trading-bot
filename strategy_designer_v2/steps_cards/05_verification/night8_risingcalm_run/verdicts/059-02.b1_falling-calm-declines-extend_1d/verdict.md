---
plan: 059-02.b1_falling-calm-declines-extend_1d
idea: 059-02.b1_falling-calm-declines-extend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 5-bar forward return on forecast (forecast < 0 grid cases): 0.000964489; OLS slope t, day-clustered: 1.06096 (threshold: slope t >= 2 (with mean short unusual move > 0) confirms; t <= -2 rejects; else inconclusive)
- Supporting check: mean unusual move in the short direction: 0.0025341, passed: True
- Counts: grid cases with forecast below 0: 608, distinct days: 246
- Decided by: The slope's t is between -2 and 2: inconclusive.
- Reading: The falling-calm profile is read from the recorded regime 'unknown' (the detector's components are not recorded and the 365-day percentile cannot be rebuilt inside a window), the situation as profile plus a negative 14-day depth, the slope t as an OLS t with standard errors clustered by calendar day, and the minimum counts as 'not observable' when not reached.
- Size: unusual move +0.41 % (t 0.84, the cases of one day together: 420 days) per case over 5 bars, 0.033 of the coin's usual move (10.60 %); normal drift in its direction -0.66 %, total -0.24 %; 655 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/059-02.b1_falling-calm-declines-extend_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-02.b1_falling-calm-declines-extend_1d`
Measure: `measure.py`
