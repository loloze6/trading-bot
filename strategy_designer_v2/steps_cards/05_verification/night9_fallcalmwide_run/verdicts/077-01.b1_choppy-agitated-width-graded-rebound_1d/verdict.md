---
plan: 077-01.b1_choppy-agitated-width-graded-rebound_1d
idea: 077-01.b1_choppy-agitated-width-graded-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return of forecast>0 cases: 0.00334415; day-clustered t: 1.00777 (threshold: confirm: mean > 0 with t >= 2 and upper-minus-lower > 0; reject: mean < 0 with t <= -2)
- Supporting check: upper minus lower half (median forecast) mean excess return: 0.000544256, passed: True
- Counts: cases: 409, distinct days: 280
- Decided by: The t lies between -2 and 2.
- Reading: Situation recomputed from prices (range over the 30-bar mean range incl. the current bar >= 1, close location < 0.5) with the choppy-agitated profile read from regime == 'unknown', on active bars where the 30-bar range mean exists; cases are bars with forecast > 0 and a next-day return in the same window; the day-clustered t uses a D/(D-1) correction; the median split puts forecast > median in the upper half and <= median in the lower half; below the plan's minimum counts the status is 'not observable'.
- Size: unusual move +0.27 % (t 0.82, the cases of one day together: 263 days) per case over 1 bars, 0.056 of the coin's usual move (5.33 %); normal drift in its direction +0.13 %, total +0.40 %; 376 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-01.b1_choppy-agitated-width-graded-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-01.b1_choppy-agitated-width-graded-rebound_1d`
Measure: `measure.py`
