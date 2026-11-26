---
plan: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
idea: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 2-bar excess return on forecast (grid bars with forecast > 0): -0.00103369; OLS slope t: -1.19584 (threshold: confirm if slope t >= 2 with mean excess > 0; reject if slope t <= -2; otherwise inconclusive)
- Supporting check: mean excess 2-bar return on the same bars: -0.00195351, passed: False
- Counts: independent grid cases with a positive forecast: 159
- Decided by: The slope t is between -2 and 2.
- Reading: Situation = 10-day over 60-day return std (ddof 1, last 60 including the last 10) above 1, recomputed from in-window closes, falling back to the recorded regime on bars without 60 in-window returns, and raw fall component below 0, on the long side; drift = the coin's mean 2-bar return on the non-overlapping grid of all its windows; slope t from a pooled OLS with intercept of excess return on forecast; the plan's 30-case minimum is applied as 'not observable' per the workflow.
- Size: unusual move -0.48 % (t -0.66, the cases of one day together: 103 days) per case over 2 bars, -0.136 of the coin's usual move (4.63 %); normal drift in its direction +0.03 %, total -0.45 %; 198 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d`
Measure: `measure.py`
