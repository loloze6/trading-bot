---
plan: 068-02_falling-agitated-run-break-fade_1d
idea: 068-02_falling-agitated-run-break-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on prior down-run length (forecast < 0): -0.0022962; slope t (day-clustered): -0.997371 (threshold: confirm: slope < 0 with t <= -2 and mean short-side unusual move > 0; reject: slope > 0 with t >= +2, or mean unusual move < 0 with t <= -2)
- Supporting check: mean short-side unusual move (drift removed, sign flipped): 0.00943373, passed: True
- Counts: cases: 759, distinct days: 387
- Decided by: Inconclusive rule: the slope t lies between -2 and +2.
- Reading: The profile is checked through the detector's regime (its vetoes send bars outside the falling agitated profile to chop and its components are not recorded), the up-close-after-down-day from prices; 'cases on the same day are summed' is read as a day-clustered standard error (scores and deviations summed per day) for the slope t and for the unusual move's t; fewer than 100 cases or 60 days is reported as not observable.
- Size: unusual move +0.94 % (t 3.26, the cases of one day together: 387 days) per case over 1 bars, 0.204 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.82 %; 759 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/068-02_falling-agitated-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/068-02_falling-agitated-run-break-fade_1d`
Measure: `measure.py`
