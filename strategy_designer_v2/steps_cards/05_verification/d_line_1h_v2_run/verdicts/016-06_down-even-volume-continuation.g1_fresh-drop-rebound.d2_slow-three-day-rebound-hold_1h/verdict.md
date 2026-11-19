---
plan: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of next-72-bar excess return on forecast (grid bars, forecast > 0): 3.92865; OLS slope t: 3.92865 (threshold: confirm if t >= 2 and supporting check > 0; reject if t <= -2; else inconclusive; at least 100 grid cases)
- Supporting check: forecast-weighted mean excess return, bar t+24 to t+72: -0.00125059, passed: False
- Counts: grid cases with forecast > 0: 1891
- Decided by: The slope's t is 2 or more but the supporting check fails (not above 0).
- Reading: Situation = recomputed 72-bar close change < 0 (recorded regime where the window lacks 72 bars) and recorded fall1d raw value < 0, expected side long; the coin's mean 72-bar and 24-to-72-bar moves are taken over all grid bars of all its windows; the plan's 'below 100 cases' rule is reported as not observable per the workflow.
Plan: `steps_cards/03_test_plan/d_line_1h_v2_run/plans/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_v2_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h`
Measure: `measure.py`
