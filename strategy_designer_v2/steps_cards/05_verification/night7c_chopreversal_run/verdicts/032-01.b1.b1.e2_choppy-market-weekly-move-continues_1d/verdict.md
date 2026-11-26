---
plan: 032-01.b1.b1.e2_choppy-market-weekly-move-continues_1d
idea: 032-01.b1.b1.e2_choppy-market-weekly-move-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed 7-bar forward return on forecast, choppy grid bars: 0.000970546; t of the OLS slope: 3.55922 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 cases)
- Supporting check: none
- Counts: non-overlapping cases on choppy bars: 1889
- Decided by: The slope is positive with t >= 2 on at least 100 cases (confirm rule).
- Reading: The 30-bar efficiency ratio is recomputed from closes inside each window, and on the first bars of a window where it cannot be, the recorded regime stands for the detector; the expected side is the sign of the recorded raw scaled 7-day move (the 7-day price return where not recorded); the coin's mean 7-bar return is taken on the non-overlapping 0,7,14,... grid of all its windows' bars; the slope's t is the ordinary least-squares slope over its standard error.
- Size: unusual move +0.50 % (t 1.32, the cases of one day together: 1091 days) per case over 7 bars, 0.035 of the coin's usual move (12.44 %); normal drift in its direction -0.01 %, total +0.49 %; 2101 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002274 on the check folds against +0.0009705 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2_choppy-market-weekly-move-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2_choppy-market-weekly-move-continues_1d`
Measure: `measure.py`
