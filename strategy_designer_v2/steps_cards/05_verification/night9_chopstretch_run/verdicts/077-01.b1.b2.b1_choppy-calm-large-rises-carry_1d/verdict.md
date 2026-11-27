---
plan: 077-01.b1.b2.b1_choppy-calm-large-rises-carry_1d
idea: 077-01.b1.b2.b1_choppy-calm-large-rises-carry
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move of long cases (return minus coin's normal 7-bar drift): 0.0146659; t of the mean, cases of one day taken together: 0.826123 (threshold: confirm: mean > 0 with day-clustered t >= 2 and correlation > 0; reject: mean < 0 with t <= -2)
- Supporting check: correlation of entry swing_rise post_pipeline_value with unusual move: 0.135944, passed: True
- Counts: cases: 76, distinct days: 64
- Decided by: t between -2 and 2: inconclusive by the plan.
- Reading: situation = swing_rise last_history_value (recomputed from closes where missing) >= 2 with regime 'trending' as the profile filter; a case is the first long bet (forecast rise >= 2 points from its low on the long side) in each 7-bar grid cell of a window, day-clustered t uses per-day summed deviations with a G/(G-1) correction, and the correlation is Pearson.
- Size: unusual move +1.47 % (t 0.83, the cases of one day together: 64 days) per case over 7 bars, 0.078 of the coin's usual move (12.84 %); normal drift in its direction +1.09 %, total +2.56 %; 76 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-01.b1.b2.b1_choppy-calm-large-rises-carry_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1.b2.b1_choppy-calm-large-rises-carry_1d`
Measure: `measure.py`
