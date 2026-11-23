---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return over bet bars (vs coin's mean daily return): 0.00302174; ordinary t of the mean: 2.31771 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: top fifth by forecast minus other four fifths, mean excess return (Welch t > 0): -1.47309, passed: False
- Counts: cases: 1717, top fifth cases: 343, other cases: 1374
- Decided by: The mean excess next-day return is above 0 with t >= 2, but the supporting check (top fifth vs other four fifths, Welch t > 0) fails.
- Reading: Situation taken as the raw surge-times-low-close product being above 0 on a long (positive) forecast bar; cases are long bets (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) with a next-day return inside the window; the top fifth is the floor(n/5) cases with the largest forecast (stable sort), the rest are the other four fifths.
- Size: unusual move +0.30 % per case over 1 bars, 0.059 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.42 %; 1717 cases
Plan: `steps_cards/03_test_plan/book_reflects_idea_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d.md`
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d`
Measure: `measure.py`
