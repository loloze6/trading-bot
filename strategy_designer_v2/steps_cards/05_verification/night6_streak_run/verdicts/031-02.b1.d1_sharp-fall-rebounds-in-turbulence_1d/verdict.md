---
plan: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
idea: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 2-bar excess return on forecast (grid bars with forecast > 0): 0.000576987; OLS slope t: 2.06353 (threshold: confirm if slope t >= 2 with mean excess > 0; reject if slope t <= -2; otherwise inconclusive)
- Supporting check: mean excess 2-bar return on the same bars: 0.00509014, passed: True
- Counts: independent grid cases with a positive forecast: 1630
- Decided by: The slope t is 2 or more and the mean excess return is above 0.
- Reading: Situation = 10-day over 60-day return std (ddof 1, last 60 including the last 10) above 1, recomputed from in-window closes, falling back to the recorded regime on bars without 60 in-window returns, and raw fall component below 0, on the long side; drift = the coin's mean 2-bar return on the non-overlapping grid of all its windows; slope t from a pooled OLS with intercept of excess return on forecast; the plan's 30-case minimum is applied as 'not observable' per the workflow.
- Size: unusual move +0.57 % (t 2.21, the cases of one day together: 960 days) per case over 2 bars, 0.085 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.81 %; 2164 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d`
Measure: `measure.py`
