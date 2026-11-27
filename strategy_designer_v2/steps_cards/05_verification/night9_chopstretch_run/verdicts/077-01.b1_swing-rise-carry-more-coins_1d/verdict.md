---
plan: 077-01.b1_swing-rise-carry-more-coins_1d
idea: 077-01.b1_swing-rise-carry-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-day move per case (return minus coin's normal 7-day drift): 0.0146659; t of the mean, cases of one day taken together: 0.826123 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 days with cases)
- Supporting check: mean unusual move, forecast at/above median minus below median: 0.0421148, passed: True
- Counts: days with cases: 64, cases: 76, active bars: 175
- Decided by: The t lies between -2 and 2 (neither the confirm nor the reject rule is met).
- Reading: A case is the first bar of each 7-bar grid cell (positions 0, 7, 14, ... of each window) on which the long forecast rises at least 2 points from its lowest level since the last such rise (from 0 after flat), with its 7-bar return inside the window; the t clusters deviations by UTC day with a D/(D-1) correction; the situation is the recorded vsr value (recomputed from prices if missing) at least 2.0 with forecast > 0.
- Size: unusual move +1.47 % (t 0.83, the cases of one day together: 64 days) per case over 7 bars, 0.078 of the coin's usual move (12.84 %); normal drift in its direction +1.09 %, total +2.56 %; 76 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-01.b1_swing-rise-carry-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1_swing-rise-carry-more-coins_1d`
Measure: `measure.py`
