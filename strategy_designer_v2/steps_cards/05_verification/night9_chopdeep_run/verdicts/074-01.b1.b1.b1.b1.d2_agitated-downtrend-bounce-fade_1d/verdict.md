---
plan: 074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual next-day move (next-day return minus coin's mean daily return, sign flipped): 0.0127264; t of the mean, cases of one day grouped: 2.28325 (threshold: confirm: mean > 0 with t >= 2 (cases of one day grouped); reject: t <= -2)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half: 0.0126491, passed: True
- Counts: cases: 433, distinct days with cases: 190
- Decided by: the mean short-side unusual move is above 0 with t >= 2 and the larger-|forecast| half beats the smaller half.
- Reading: Cases are short bets (forecast moving at least 2 points further short from its lowest short level since the last bet, from 0 after flat or a side change) with the coin's mean taken over all next-day returns of all its windows, the t uses per-day summed deviations with a D/(D-1) correction, the median split puts ties in the smaller half, and the situation check uses the adapted regime's three conditions (the profile veto only narrows it).
- Size: unusual move +1.27 % (t 2.29, the cases of one day together: 190 days) per case over 1 bars, 0.260 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +1.14 %; 433 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01043 on the check folds against +0.01273 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade_1d`
Measure: `measure.py`
