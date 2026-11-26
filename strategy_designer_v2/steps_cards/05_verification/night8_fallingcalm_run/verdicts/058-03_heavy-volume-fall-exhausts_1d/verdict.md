---
plan: 058-03_heavy-volume-fall-exhausts_1d
idea: 058-03_heavy-volume-fall-exhausts
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar forward return, heavy minus quiet volume: -0.0129266; Welch t: -0.975751 (threshold: difference > 0 with Welch t >= 2 confirms; < 0 with t <= -2 rejects; at least 30 cases per group)
- Supporting check: none
- Counts: heavy-volume cases (forecast > 0): 58, quiet-volume cases (forecast < 0): 408
- Decided by: Welch t lies between -2 and 2 (inconclusive rule).
- Reading: The situation is checked on active bars whose 30-bar return can be computed inside their window (30-bar return < 0 from closes, with the falling-calm profile taken from the recorded regime 'mean_reversion' since its components are not recorded), and the expected side is the sign of the raw log volume ratio (heavier than the 365-bar mean = long); cases are the bars at positions 0, 5, 10, ... of each window with regime 'mean_reversion', a non-zero forecast and a close 5 bars later in the same window, and the plan's 'fewer than 30 cases in either group' is applied as the minimum count giving 'not observable'.
- Size: unusual move +0.08 % (t 0.13, the cases of one day together: 305 days) per case over 5 bars, 0.017 of the coin's usual move (10.60 %); normal drift in its direction -0.49 %, total -0.41 %; 388 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-03_heavy-volume-fall-exhausts_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-03_heavy-volume-fall-exhausts_1d`
Measure: `measure.py`
