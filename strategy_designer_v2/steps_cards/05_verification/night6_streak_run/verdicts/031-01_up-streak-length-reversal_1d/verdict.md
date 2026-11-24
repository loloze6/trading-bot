---
plan: 031-01_up-streak-length-reversal_1d
idea: 031-01_up-streak-length-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per short case, short direction, before costs: 0.00321418; t of the mean, cases clustered by day: 1.08379 (threshold: day-clustered t >= 2 to confirm, <= -2 to reject, on at least 100 cases over at least 30 days)
- Supporting check: mean unusual short move of top third of |forecast| minus bottom third: -0.00173518, passed: False
- Counts: cases: 3132, days: 1206
- Decided by: The main measure's t is strictly between -2 and 2.
- Reading: Situation = close above the previous close inside the window (raw rank > 0 on a window's first bar), side short; a case is the first short bet in each 5-bar grid cell of its window (bet = |forecast| rising >= 2 from its lowest level on the short side since the last bet, reset after flat or side change), its return taken from that bar's close 5 bars ahead inside the window; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the thirds are the n//3 cases with the largest and smallest |forecast|.
- Size: unusual move +0.32 % (t 1.08, the cases of one day together: 1206 days) per case over 5 bars, 0.035 of the coin's usual move (10.60 %); normal drift in its direction -0.66 %, total -0.34 %; 3132 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01_up-streak-length-reversal_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01_up-streak-length-reversal_1d`
Measure: `measure.py`
