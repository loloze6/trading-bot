---
plan: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
idea: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 2-bar excess return on forecast (grid bars with forecast > 0): 0.000967334; OLS slope t: 0.818012 (threshold: confirm if slope t >= 2 with mean excess > 0; reject if slope t <= -2; otherwise inconclusive)
- Supporting check: mean excess 2-bar return on the same bars: 0.00503279, passed: True
- Counts: independent grid cases with a positive forecast: 238
- Decided by: The slope t is between -2 and 2.
- Reading: Situation = 10-day over 60-day return std (ddof 1, last 60 including the last 10) above 1, recomputed from in-window closes, falling back to the recorded regime on bars without 60 in-window returns, and raw fall component below 0, on the long side; drift = the coin's mean 2-bar return on the non-overlapping grid of all its windows; slope t from a pooled OLS with intercept of excess return on forecast; the plan's 30-case minimum is applied as 'not observable' per the workflow.
- Size: unusual move +0.79 % (t 0.81, the cases of one day together: 204 days) per case over 2 bars, 0.063 of the coin's usual move (11.42 %); normal drift in its direction +1.94 %, total +2.74 %; 316 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2016_2017/backtests/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d`
Measure: `measure.py`
