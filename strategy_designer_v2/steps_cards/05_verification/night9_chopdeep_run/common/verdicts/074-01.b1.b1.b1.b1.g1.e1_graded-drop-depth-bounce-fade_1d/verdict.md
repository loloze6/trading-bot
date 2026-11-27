---
plan: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move in the short direction on forecast<0 bars: 0.00509982; t of the mean, cases summed per day: 1.634 (threshold: confirm: mean > 0 with t >= 2 over >= 100 distinct days and upper half beats lower half; reject: mean < 0 with t <= -2 over >= 100 distinct days)
- Supporting check: mean unusual move, upper minus lower half of abs(forecast): 0.0128395, passed: True
- Counts: distinct case days: 639, cases: 1866
- Decided by: The t of the mean unusual move lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: Situation computed from prices as 1-day return > 0 and high-low range above its 20-bar mean (bar t included), falling back to regime=='trending' on the first bars of a window where it cannot be computed, side short (forecast < 0); coin mean daily return is the mean of all within-window next-day returns over all its windows; t clusters cases by UTC date; the median split puts abs(forecast) > median in the upper half and <= median in the lower half.
- Size: unusual move +0.61 % (t 1.85, the cases of one day together: 552 days) per case over 1 bars, 0.117 of the coin's usual move (5.44 %); normal drift in its direction -0.13 %, total +0.47 %; 1574 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/common/backtests/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d`
Measure: `measure.py`
