---
plan: 050-04.b1_range-scaled-week-rise-more-coins_1d
idea: 050-04.b1_range-scaled-week-rise-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of the cases (long): 0.00630669; t of the mean, cases of one day taken together: 1.83431 (threshold: confirm: mean > 0 with t >= 2 (day-clustered); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on case-bar post_pipeline_value: -0.000368685, passed: False
- Counts: cases: 496, distinct days: 342
- Decided by: Neither the confirm nor the reject rule is met (the mean is not above 0 with t >= 2).
- Reading: The falling-calm profile is read from the recorded regime ('unknown' = neither veto fired) and the 7-day rise from the raw component sign (price 7-day return where unrecorded); a case is the first bet (forecast rise >= 2 points from its lowest long level since the last bet, reset at 0) in each 3-bar grid cell from each window's first row; the day-clustered t uses the D/(D-1) correction; the slope t is the ordinary OLS t; unmet minimum counts give 'not observable' per the workflow.
- Size: unusual move +0.63 % (t 1.84, the cases of one day together: 342 days) per case over 3 bars, 0.077 of the coin's usual move (8.43 %); normal drift in its direction +0.34 %, total +0.97 %; 496 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.834 (not below 1), 496 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-04.b1_range-scaled-week-rise-more-coins_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-04.b1_range-scaled-week-rise-more-coins_1d`
Measure: `measure.py`
