---
plan: 033-01.g1_wide-day-low-close-rebound_1d
idea: 033-01.g1_wide-day-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 96 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-day excess return on forecast: 0.000628257; slope t, cases of one day summed: 3.19377 (threshold: confirm: t >= 2 with top-minus-bottom fifth > 0; reject: t <= -2)
- Supporting check: top fifth minus bottom fifth mean next-day excess return: 0.00609663, passed: True
- Counts: bars with |forecast| >= 2: 8681, distinct days: 2898, cases: 17380
- Decided by: Slope t >= 2 and the top-minus-bottom-fifth difference is above 0 (confirm rule).
- Reading: Every bar with a forecast and a next-day return inside its window is a case (forecast-0 bars included); the day-clustered slope t uses residual-times-forecast deviations summed per UTC day with a G/(G-1) correction; fifths are the pooled 20th/80th forecast percentiles; the plan's minimum counts, if not reached, give 'not observable' as the workflow requires.
- Size: unusual move +0.25 % (t 2.54, the cases of one day together: 2358 days) per case over 1 bars, 0.055 of the coin's usual move (4.78 %); normal drift in its direction +0.00 %, total +0.25 %; 7047 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001964 on the check folds against +0.0006283 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/033-01.g1_wide-day-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-01.g1_wide-day-low-close-rebound_1d`
Measure: `measure.py`
