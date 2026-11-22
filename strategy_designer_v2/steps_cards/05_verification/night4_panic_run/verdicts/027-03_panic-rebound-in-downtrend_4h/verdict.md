---
plan: 027-03_panic-rebound-in-downtrend_4h
idea: 027-03_panic-rebound-in-downtrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 84-bar move per case (return minus coin's normal 84-bar drift): 0.0223027; t of the mean: 0.985277 (threshold: confirm: mean > 0 with t >= 2 on >= 20 independent cases and supporting check passes; reject: mean < 0 with t <= -2 on >= 20 cases)
- Supporting check: forecast-weighted case mean minus unweighted mean (>= 0 passes): 0, passed: True
- Counts: independent cases: 40, active bars: 187
- Decided by: The t lies between -2 and 2 on at least 20 cases.
- Reading: Situation recomputed per window from prices (prior return close[t-6]/close[t-186]-1 < 0, bar range (high-low)/close with 180-bar mean / 6-bar mean <= 0.3333, and a fall: the recorded raw 'fall' value, else the 6-bar return, < 0), using the recorded regime for the prior/range rules on bars too early in a window to recompute them; cases are the first long bet (forecast rise >= 2 from its low since the last bet) in each 84-bar grid cell of a window, with a full 84-bar forward return, and the normal drift is the coin's mean 84-bar grid return over all its windows.
- Size: unusual move +2.23 % per case over 84 bars, 0.076 of the coin's usual move (17.66 %); normal drift in its direction +2.03 %, total +4.26 %; 40 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend_4h`
Measure: `measure.py`
