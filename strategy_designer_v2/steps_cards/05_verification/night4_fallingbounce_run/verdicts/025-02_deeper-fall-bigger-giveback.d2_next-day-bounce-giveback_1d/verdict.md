---
plan: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d
idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day fall over short bets (sign flipped, minus coin mean daily return): 0.00268545; t of the mean: 2.39918 (threshold: confirm t >= 2, reject t <= -2, over at least 30 cases)
- Supporting check: top-half minus bottom-half |forecast| mean excess fall, Welch t > 0: -0.529324, passed: False
- Counts: cases: 1428, top-half cases: 714, bottom-half cases: 714
- Decided by: Main t >= 2 but the size check fails (top-half minus bottom-half Welch t not > 0).
- Reading: A case is a bet as in the workflow's holding-period rule (the short forecast deepening by >= 2 points from its lowest short level since its last bet, reset to 0 after a flat or side change), the situation is a 90-day return below 0 (recomputed from closes inside the window where 90 prior bars exist, else the recorded regime) with a positive raw scaled one-day return, and the top half is the n//2 cases with the largest |forecast| (ties by time order), the rest the bottom half.
- Size: unusual move +0.27 % per case over 1 bars, 0.058 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.15 %; 1428 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d`
Measure: `measure.py`
