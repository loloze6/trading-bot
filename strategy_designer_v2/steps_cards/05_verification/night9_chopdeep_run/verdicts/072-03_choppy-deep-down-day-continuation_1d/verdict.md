---
plan: 072-03_choppy-deep-down-day-continuation_1d
idea: 072-03_choppy-deep-down-day-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain per case (position x next-day excess return): 3.68859e-05; t of the mean, cases of one day summed: 0.0371877 (threshold: confirm: mean > 0 with t >= 2 (and supporting check < 0); reject: mean < 0 with t <= -2; at least 100 cases on 100 distinct days)
- Supporting check: deeper-half minus shallower-half mean next-day excess return (split at median |forecast|): 0.000868211, passed: False
- Counts: cases: 1885, distinct days: 1108
- Decided by: The t of the mean timing gain lies between -2 and 2, so the result is inconclusive.
- Reading: Cases are bars with a nonzero position after the trade and a next close in the same window; the t sums each day's deviations across coins into one piece of evidence; the deeper half is |forecast| strictly above the median, the shallower half at or below it; the choppy profile is read from the detector's regime column, the down close from the prices.
- Size: unusual move -0.10 % (t -0.73, the cases of one day together: 926 days) per case over 1 bars, -0.008 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total -0.21 %; 1476 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-03_choppy-deep-down-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03_choppy-deep-down-day-continuation_1d`
Measure: `measure.py`
