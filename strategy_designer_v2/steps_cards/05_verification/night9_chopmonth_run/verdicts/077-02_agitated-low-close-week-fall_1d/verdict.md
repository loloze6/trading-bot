---
plan: 077-02_agitated-low-close-week-fall_1d
idea: 077-02_agitated-low-close-week-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move in the short direction (return minus coin drift): 0.00650169; t of the mean, cases of one day summed: 0.994816 (threshold: confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: 0.0077455, passed: True
- Counts: cases: 1738, distinct case days: 679
- Decided by: The t lies between -2 and 2.
- Reading: Agitation for the situation check is the regime not being the veto's 'chop'; a case is the first short bet in each 7-bar grid cell (cases whose 7-bar return leaves the window are dropped); the halves are the n//2 cases with the largest and the n//2 with the smallest |forecast| (middle case dropped if n is odd); the t uses a day-clustered standard error; fewer than 30 case days is reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +0.65 % (t 1.00, the cases of one day together: 679 days) per case over 7 bars, 0.051 of the coin's usual move (12.84 %); normal drift in its direction -1.01 %, total -0.36 %; 1738 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/077-02_agitated-low-close-week-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/077-02_agitated-low-close-week-fall_1d`
Measure: `measure.py`
