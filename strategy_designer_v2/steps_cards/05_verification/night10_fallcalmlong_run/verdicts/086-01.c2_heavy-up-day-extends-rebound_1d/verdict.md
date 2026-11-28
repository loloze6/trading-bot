---
plan: 086-01.c2_heavy-up-day-extends-rebound_1d
idea: 086-01.c2_heavy-up-day-extends-rebound
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-day move of bets (return minus coin's normal 10-day drift): 0.011277; t of the mean, cases of one day as one: 0.684099 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman(heavy_volume raw ratio, unusual move) > 0: 0.0301004, passed: True
- Counts: cases: 96, days: 82
- Decided by: t lies between -2 and 2 (or is not computable): neither confirmed nor rejected. No effect (common/verdicts.md): t in the idea's direction +0.684 (below 1), 96 cases (30 needed).
- Reading: The situation is checked on its three day conditions (1-day return > 0, volume ratio >= 1.5 from the recorded heavy_volume raw value or the prices, close[t-1]/close[t-6]-1 > 0) with a long side, the profile being added by code and not recomputable within a window, and active bars whose conditions cannot be computed inside their window are left out; a case is the first bet (forecast rise >= 2 from its lowest positive level since its last bet, from 0 after a flat) in each 10-bar grid cell of a window with a full 10-bar return ahead; the day-clustered t is mean / (sqrt(sum of per-day summed deviations^2) / n) with a D/(D-1) correction.
- Size: unusual move +1.13 % (t 0.69, the cases of one day together: 82 days) per case over 10 bars, 0.083 of the coin's usual move (16.20 %); normal drift in its direction +1.16 %, total +2.29 %; 96 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.684 (below 1), 96 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/086-01.c2_heavy-up-day-extends-rebound_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-01.c2_heavy-up-day-extends-rebound_1d`
Measure: `measure.py`
