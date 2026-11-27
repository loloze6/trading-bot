---
plan: 070-01.g1.d2.d1_depth-graded-run-break-fade_1d
idea: 070-01.g1.d2.d1_depth-graded-run-break-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: next-day short-direction return minus coin mean daily return on event bars: 0.0059314; t of the mean (per-day sums): 3.53562 (threshold: mean > 0 with t >= 2 confirms; t <= -2 rejects)
- Supporting check: deeper-half minus shallower-half mean short excess return (split at median |forecast|): None, passed: None
- Counts: event bars: 2126, distinct days: 922
- Decided by: Inconclusive rule: the main measure confirms but the deeper-minus-shallower difference is at or below 0 with Welch t above -2.
- Reading: Situation = up close after at least 2 strictly lower consecutive closes inside the window (first 3 rows of a window use the recorded run loss > 0 instead); main mean is the mean over cases and its t is on per-day sums; deeper half = |forecast| strictly above the median; the plan's minimum counts (100 event bars with a next-day return, 80 distinct days) give 'not observable'.
- Size: unusual move +0.59 % (t 3.56, the cases of one day together: 920 days) per case over 1 bars, 0.125 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.47 %; 2123 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.g1.d2.d1_depth-graded-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d2.d1_depth-graded-run-break-fade_1d`
Measure: `measure.py`
