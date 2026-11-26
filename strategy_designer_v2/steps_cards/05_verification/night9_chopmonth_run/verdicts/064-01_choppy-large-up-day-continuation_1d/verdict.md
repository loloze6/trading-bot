---
plan: 064-01_choppy-large-up-day-continuation_1d
idea: 064-01_choppy-large-up-day-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean strength of long cases over 5 bars (unusual move / usual 5-bar move): -0.02397; t of the mean, cases grouped by day: -0.201982 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above-median forecast minus at/below-median: 0.0373806, passed: True
- Counts: cases: 259, distinct days: 174
- Decided by: The t of the mean strength is between -2 and 2.
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest long level since the last bet) in each 5-bar grid cell of a window, the day t uses the day-summed deviations with a D/(D-1) correction, the supporting check uses the unusual move (not divided by the usual move), and fewer than 30 cases or 30 days is reported as not observable.
- Size: unusual move +1.25 % (t 0.64, the cases of one day together: 174 days) per case over 5 bars, -0.024 of the coin's usual move (12.35 %); normal drift in its direction +0.82 %, total +2.08 %; 259 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/064-01_choppy-large-up-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/064-01_choppy-large-up-day-continuation_1d`
Measure: `measure.py`
