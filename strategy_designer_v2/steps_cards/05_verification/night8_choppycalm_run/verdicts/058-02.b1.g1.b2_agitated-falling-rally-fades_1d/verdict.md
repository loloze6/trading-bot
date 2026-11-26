---
plan: 058-02.b1.g1.b2_agitated-falling-rally-fades_1d
idea: 058-02.b1.g1.b2_agitated-falling-rally-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of demeaned next-day return on post_pipeline_value (forecast < 0): -0.000151919; t, errors clustered by day: -0.490238 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean unusual move in the short direction: 0.0055899, passed: True
- Counts: bars with a forecast below 0: 1326, distinct days: 633
- Decided by: the t of the slope lies between -2 and 2
- Reading: the profile is read from the recorded regime ('unknown' = neither chop veto fired) and the rise from the recorded raw value (1-bar return when unrecorded); the coin's mean daily return is the mean of all its within-window next-day returns; the slope is OLS with intercept and CR1 day-clustered errors; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' as the workflow requires
- Size: unusual move +0.61 % (t 2.38, the cases of one day together: 445 days) per case over 1 bars, 0.131 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.48 %; 857 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b2_agitated-falling-rally-fades_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b2_agitated-falling-rally-fades_1d`
Measure: `measure.py`
