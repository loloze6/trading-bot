---
plan: 027-02_panic-fall-depth-rebound_4h
idea: 027-02_panic-fall-depth-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 84-bar excess return (in usual moves) on 6-bar fall depth: 0.00586737; OLS slope t: 0.493547 (threshold: confirm: slope > 0 with t >= 2, mean excess > 0, >= 30 cases; reject: slope < 0 with t <= -2, >= 30 cases)
- Supporting check: mean excess return of the cases above 0: 0.151294, passed: True
- Counts: cases: 142
- Decided by: The slope t lies between -2 and 2.
- Reading: Situation recomputed as mean(high-low) over the last 6 bars >= 3x its 180-bar mean within each window (the regime column where history is too short), side long on a negative 6-bar change; a case is a holding-period bet (forecast rise >= 2 points) in the mean_reversion regime, the first per 84-bar grid cell counted from each window's first row, cases without close[t+84] in the window dropped; the coin's drift and usual move are the mean and standard deviation of its 84-bar returns on that grid over all windows; the slope's t is the ordinary OLS t; fewer than 30 cases gives 'not observable'.
- Size: unusual move +3.44 % per case over 84 bars, 0.151 of the coin's usual move (17.66 %); normal drift in its direction +2.27 %, total +5.71 %; 142 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-02_panic-fall-depth-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound_4h`
Measure: `measure.py`
