---
plan: 059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks_1d
idea: 059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 21-bar excess return on forecast: 0.0076227; day-clustered slope t: 2.00035 (threshold: slope t >= 2 to confirm (with mean excess > 0); slope t <= -2 or mean excess t <= -2 to reject)
- Supporting check: mean 21-bar excess return of cases: -0.00611487, passed: False
- Counts: cases: 103, distinct days: 48
- Decided by: Slope t is 2 or more but the mean excess return is 0 or below: inconclusive.
- Reading: Profile read from the recorded regime ('unknown' = choppy calm); cases are grid bars (0,21,42,... per window) with forecast > 0 and a full 21-bar forward return in the window; normal drift is the coin's mean non-overlapping 21-bar return over all its windows; slope and mean t use day-clustered standard errors (CR0, deviations summed per day) without small-sample correction.
- Size: unusual move -0.88 % (t -0.59, the cases of one day together: 309 days) per case over 21 bars, -0.051 of the coin's usual move (27.91 %); normal drift in its direction +4.06 %, total +3.18 %; 467 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks_1d`
Measure: `measure.py`
