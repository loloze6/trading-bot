---
plan: 077-03.g1_choppy-agitated-high-close-fall_1d
idea: 077-03.g1_choppy-agitated-high-close-fall
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return minus coin drift, short direction, per short bet: 0.00792949; t of the mean, cases of one day taken together: 3.26024 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting diff > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual short move, larger |forecast| half minus smaller half: -0.00177754, passed: False
- Counts: cases: 538, distinct days: 355
- Decided by: The main measure is positive with t >= 2 but the supporting difference is not above 0.
- Reading: The profile is read from the regime column (not 'chop' = inside the choppy agitated profile) and the close location recomputed from prices; a case is a bet per the workflow's holding rule (short forecast rising by >= 2 points from its lowest level since the last bet, from 0 after flat or a side change) on the 1-bar grid; the day-clustered t uses a D/(D-1) correction; the median split puts |forecast| above the median in the larger half and at or below it in the smaller half; the plan's '<100 cases or <60 days' rule is reported as 'not observable'.
- Size: unusual move +0.79 % (t 3.26, the cases of one day together: 355 days) per case over 1 bars, 0.175 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.67 %; 538 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03.g1_choppy-agitated-high-close-fall_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.g1_choppy-agitated-high-close-fall_1d`
Measure: `measure.py`
