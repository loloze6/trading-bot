---
plan: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 72-bar excess return on forecast (forecast > 0 grid bars): 0.000588102; OLS slope t: 2.62733 (threshold: slope t >= 2 confirms (with supporting check), t <= -2 rejects; at least 100 grid cases with forecast > 0)
- Supporting check: mean excess 72-bar return of top third of forecast > 0: 0.00469554, passed: True
- Counts: independent grid cases with a positive forecast: 2762, top third cases: 921
- Decided by: The slope's t is 2.63 (>= 2) and the top third's mean excess return is above 0.
- Reading: Grid is positions 0, 72, 144, ... of each window; the coin's mean 72-bar return is the mean over all its grid bars in all windows; top third is forecast at or above its 2/3 quantile among the positive-forecast samples.
- Size: unusual move -0.27 % per case over 72 bars, -0.033 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.14 %; 4750 cases
Plan: `steps_cards/03_test_plan/hold_ideas_1h_run/plans/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h.md`
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h`
Measure: `measure.py`
