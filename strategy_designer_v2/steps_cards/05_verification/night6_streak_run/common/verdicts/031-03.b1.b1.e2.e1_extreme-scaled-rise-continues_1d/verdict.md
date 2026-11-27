---
plan: 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d
idea: 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move per long case: 0.0238154; t of the mean, cases pooled by day: 3.10315 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: mean unusual move, top third by forecast minus bottom third: 0.0258719, passed: True
- Counts: distinct case days: 833, cases: 1730
- Decided by: Mean unusual move above 0 with t >= 2 and the top-minus-bottom-third check above 0.
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest long level since the last bet) in each 10-bar grid cell of a window, its return taken from that bar's close 10 bars ahead within the window, the drift is the mean of the coin's grid 10-bar returns over all its windows, and the thirds are floor(n/3) cases at each end of the forecast ranking.
- Size: unusual move +2.38 % (t 3.11, the cases of one day together: 833 days) per case over 10 bars, 0.119 of the coin's usual move (16.72 %); normal drift in its direction +1.44 %, total +3.82 %; 1730 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/common/backtests/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d`
Measure: `measure.py`
