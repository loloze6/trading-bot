---
plan: 067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins_1d
idea: 067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction (day-clustered): 0.00480145; t of the mean, cases of one day taken together: 0.841609 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger half of |forecast| minus smaller half: -0.026755, passed: False
- Counts: cases: 407, distinct days: 297
- Decided by: The t is between -2 and 2.
- Reading: A case is the first short bet (forecast magnitude rising at least 2 points above its lowest level since the last bet, from 0 after a flat) in each 5-bar grid cell of a window, needing 5 bars after it; the profile is the record's regime not 'chop'; the halves of |forecast| are its lower and upper n//2 ranked cases (the middle case dropped when n is odd); the day-clustered t uses the G/(G-1) correction.
- Size: unusual move +0.48 % (t 0.84, the cases of one day together: 297 days) per case over 5 bars, 0.029 of the coin's usual move (11.70 %); normal drift in its direction -0.69 %, total -0.21 %; 407 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins_1d`
Measure: `measure.py`
