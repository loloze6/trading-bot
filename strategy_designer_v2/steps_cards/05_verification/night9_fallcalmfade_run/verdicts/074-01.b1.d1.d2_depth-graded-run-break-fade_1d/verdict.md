---
plan: 074-01.b1.d1.d2_depth-graded-run-break-fade_1d
idea: 074-01.b1.d1.d2_depth-graded-run-break-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return minus coin mean, short direction, on forecast < 0: 0.00921947; t of the mean, cases summed per day: 3.53551 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: t <= -2)
- Supporting check: excess return top half minus bottom half of |forecast|: 0.0119105, passed: True
- Counts: independent case-days: 426, cases: 834, active bars: 839
- Decided by: Mean short-direction excess return > 0 with t >= 2 and the top-half minus bottom-half difference > 0.
- Reading: Profile is the 60-bar close change in percent below -10 and the down-run is counted from closes inside the window, falling back to the recorded regime where the window lacks the history; t clusters cases by UTC day (deviations summed per day); top half of |forecast| is cases above the median |forecast|, bottom half at or below; fewer than 30 case-days is reported as not observable.
- Size: unusual move +0.91 % (t 3.49, the cases of one day together: 423 days) per case over 1 bars, 0.189 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.79 %; 829 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003652 on the check folds against +0.009219 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d1.d2_depth-graded-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d1.d2_depth-graded-run-break-fade_1d`
Measure: `measure.py`
