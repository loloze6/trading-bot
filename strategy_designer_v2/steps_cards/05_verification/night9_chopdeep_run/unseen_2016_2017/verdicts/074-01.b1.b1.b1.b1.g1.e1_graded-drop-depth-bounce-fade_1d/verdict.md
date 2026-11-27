---
plan: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move in the short direction on forecast<0 bars: -0.00116188; t of the mean, cases summed per day: -0.169466 (threshold: confirm: mean > 0 with t >= 2 over >= 100 distinct days and upper half beats lower half; reject: mean < 0 with t <= -2 over >= 100 distinct days)
- Supporting check: mean unusual move, upper minus lower half of abs(forecast): 0.00338168, passed: True
- Counts: distinct case days: 31, cases: 33
- Decided by: Only 31 distinct case days, below the plan's minimum of 100.
- Reading: Situation computed from prices as 1-day return > 0 and high-low range above its 20-bar mean (bar t included), falling back to regime=='trending' on the first bars of a window where it cannot be computed, side short (forecast < 0); coin mean daily return is the mean of all within-window next-day returns over all its windows; t clusters cases by UTC date; the median split puts abs(forecast) > median in the upper half and <= median in the lower half.
- Size: unusual move -0.49 % (t -0.63, the cases of one day together: 24 days) per case over 1 bars, -0.062 of the coin's usual move (7.55 %); normal drift in its direction -1.05 %, total -1.54 %; 26 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d`
Measure: `measure.py`
