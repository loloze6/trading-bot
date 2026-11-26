---
plan: 067-01.b1.g1.b1_choppy-month-fall-continues_1d
idea: 067-01.b1.g1.b1_choppy-month-fall-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move in the short direction of the short bets: 0.0139983; t clustered by day: 2.07387 (threshold: confirm: mean > 0 with day-clustered t >= 2 and size correlation > 0; reject: mean < 0 with t <= -2)
- Supporting check: correlation of |forecast| with the unusual short move: 0.0583654, passed: True
- Counts: cases: 850, distinct days: 522
- Decided by: The mean unusual short move is positive with t >= 2 and the size correlation is above 0.
- Reading: Choppy is read as the bars whose regime is 'unknown' (the config's only traded regime, the trend vetoes giving 'chop'); a case is the first short bet (forecast more negative by >= 2 points from its smallest short size since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, dropped if its 10-bar return leaves the window; drift is the coin's mean 10-bar return on the grid of all its windows; the day-clustered t uses the sum of deviations per UTC day with a G/(G-1) correction; the 30-distinct-day minimum gives 'not observable'.
- Size: unusual move +1.40 % (t 2.08, the cases of one day together: 522 days) per case over 10 bars, 0.072 of the coin's usual move (16.82 %); normal drift in its direction -1.50 %, total -0.10 %; 850 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.006569 on the check folds against +0.014 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1_choppy-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1_choppy-month-fall-continues_1d`
Measure: `measure.py`
