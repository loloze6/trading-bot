---
plan: 086-02.c2_quiet-three-day-rise-continuation_1d
idea: 086-02.c2_quiet-three-day-rise-continuation
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast, trending grid cases: 4.26114e-05; OLS slope t: 0.0491026 (threshold: slope t >= 2 (with >= 30 cases forecast > 0 and check passing) confirms; <= -2 rejects)
- Supporting check: mean excess 5-bar return of grid cases with forecast > 0 above 0: -0.00200661, passed: False
- Counts: grid cases in the regime: 302, grid cases with forecast > 0: 184, active bars: 973
- Decided by: Slope t is between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.049 (below 1), 184 cases (30 needed).
- Reading: Cases are the regime-'trending' bars at grid positions 0,5,10,... of each window with a 5-bar forward return inside the window, the regression includes their zero forecasts, the coin's mean 5-bar return is taken on the same grid over all bars of all its windows, the profile is read from the recorded regime, and the plan's 'too few cases' rule is reported as 'not observable'.
- Size: unusual move +0.25 % (t 0.41, the cases of one day together: 312 days) per case over 5 bars, 0.025 of the coin's usual move (11.31 %); normal drift in its direction +0.60 %, total +0.84 %; 416 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.049 (below 1), 184 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/086-02.c2_quiet-three-day-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-02.c2_quiet-three-day-rise-continuation_1d`
Measure: `measure.py`
