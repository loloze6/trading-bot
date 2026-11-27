---
plan: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move in the short direction on forecast<0 bars: 0.00818129; t of the mean, cases summed per day: 2.22737 (threshold: confirm: mean > 0 with t >= 2 over >= 100 distinct days and upper half beats lower half; reject: mean < 0 with t <= -2 over >= 100 distinct days)
- Supporting check: mean unusual move, upper minus lower half of abs(forecast): 0.0138109, passed: True
- Counts: distinct case days: 446, cases: 1122
- Decided by: Mean unusual move above 0 with t >= 2 over at least 100 distinct days, and the upper half of abs(forecast) beats the lower half.
- Reading: Situation computed from prices as 1-day return > 0 and high-low range above its 20-bar mean (bar t included), falling back to regime=='trending' on the first bars of a window where it cannot be computed, side short (forecast < 0); coin mean daily return is the mean of all within-window next-day returns over all its windows; t clusters cases by UTC date; the median split puts abs(forecast) > median in the upper half and <= median in the lower half.
- Size: unusual move +0.95 % (t 2.48, the cases of one day together: 388 days) per case over 1 bars, 0.183 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.80 %; 957 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.006848 on the check folds against +0.008181 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d`
Measure: `measure.py`
