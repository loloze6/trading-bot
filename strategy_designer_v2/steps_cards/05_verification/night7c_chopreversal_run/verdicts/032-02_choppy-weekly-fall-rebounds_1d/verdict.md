---
plan: 032-02_choppy-weekly-fall-rebounds_1d
idea: 032-02_choppy-weekly-fall-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered t of the slope of 7-bar excess return on forecast: 0.00103889; day-clustered slope t: 1.00582 (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2)
- Supporting check: mean excess 7-bar return of the cases > 0 (its day-clustered t: -1.283): -0.0122493, passed: False
- Counts: cases: 444, cases on distinct days: 196
- Decided by: Inconclusive: the slope's t is between -2 and 2, and the mean excess t is above -2.
- Reading: The regime part of the situation (30-day efficiency ratio <= 0.3 and 30-day volatility at or above its one-year median) is read from the recorded `regime` (the detector is not recorded and 365 days of history are not in a window), with the efficiency ratio also recomputed from in-window prices where 30 prior bars exist; the fall is the recorded raw scaled 7-day return below 0; the slope t is OLS with intercept and day-clustered standard errors; the plan's 'fewer than 40 cases on distinct days' is applied as the minimum count (not observable).
- Size: unusual move -0.84 % (t -1.23, the cases of one day together: 454 days) per case over 7 bars, -0.057 of the coin's usual move (12.44 %); normal drift in its direction +0.97 %, total +0.13 %; 710 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-02_choppy-weekly-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-02_choppy-weekly-fall-rebounds_1d`
Measure: `measure.py`
