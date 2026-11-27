---
plan: 067-02.b1.b1.d1.g1_choppy-agitated-month-falls-continue_1d
idea: 067-02.b1.b1.d1.g1_choppy-agitated-month-falls-continue
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move per case, short direction, 7 bars: 0.0053883; t of the mean, cases clustered by day: 0.430189 (threshold: confirm: mean > 0 with t >= 2 and deeper-minus-shallower > 0; reject: mean < 0 with t <= -2)
- Supporting check: deeper-half minus shallower-half mean unusual move: 0.0235737, passed: True
- Counts: cases: 215, days: 108
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Choppy agitated is read as the detector's 'unknown' regime (the only regime with a strategy) and the month fall as the raw 30-bar return < 0 (from prices where not recorded); the coin's mean 7-bar return is taken on the same non-overlapping grid over all its windows; t clusters cases by UTC day (deviations summed per day); the median split puts forecasts <= median in the deeper half and > median in the shallower half.
- Size: unusual move +1.22 % (t 1.66, the cases of one day together: 265 days) per case over 7 bars, 0.076 of the coin's usual move (12.84 %); normal drift in its direction -0.94 %, total +0.28 %; 359 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.d1.g1_choppy-agitated-month-falls-continue_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d1.g1_choppy-agitated-month-falls-continue_1d`
Measure: `measure.py`
