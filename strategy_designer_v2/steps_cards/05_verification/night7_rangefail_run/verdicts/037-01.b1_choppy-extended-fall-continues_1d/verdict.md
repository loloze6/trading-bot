---
plan: 037-01.b1_choppy-extended-fall-continues_1d
idea: 037-01.b1_choppy-extended-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per short case (short direction): 0.00631214; t of the mean, cases of one day taken together: 1.35827 (threshold: t >= 2 (with slope > 0) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: OLS slope of unusual move on forecast size: -0.000407479, passed: False
- Counts: cases: 994, distinct days: 567
- Decided by: The t of the mean unusual move lies between -2 and 2 (inconclusive rule).
- Reading: Situation = raw fall_in_swings < 0 and 20-bar return < 0 recomputed from the window's closes (the recorded regime 'trending' stands in on the first 20 bars of a window), side short, the choppy profile not checked since the plan adds it by code; a case is a short bet (forecast growing more negative by at least 2 points from its smallest short size since the last bet, from 0 after a flat or side change), the first one in each 5-bar grid cell of its window, needing close 5 bars later in the same window; drift = mean of the coin's non-overlapping 5-bar grid returns over all its windows; t = mean over a day-clustered standard error (deviations summed per day, D/(D-1) correction); the slope is OLS of the unusual move on |forecast| at the case bar.
- Size: unusual move +0.63 % (t 1.36, the cases of one day together: 567 days) per case over 5 bars, 0.044 of the coin's usual move (12.35 %); normal drift in its direction -0.79 %, total -0.16 %; 994 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/037-01.b1_choppy-extended-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/037-01.b1_choppy-extended-fall-continues_1d`
Measure: `measure.py`
