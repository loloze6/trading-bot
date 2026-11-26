---
plan: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d
idea: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 20-bar excess return on raw brk_runup weight: -1.0319; slope t (day-clustered): -1.0319 (threshold: t >= 2 with positive supporting check confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean excess 20-bar return of cases with weight > 0: 0.129145, passed: True
- Counts: breakout cases: 114, cases with weight above 0: 60, days: 84
- Decided by: The slope's t is between -2 and 2.
- Reading: Breakouts are recomputed only on bars with 60 prior closes in the same window, so active bars without that history are left out of the agreement share; the 20-bar grid starts at each window's first row and a case needs its forward close inside the window; the slope's t uses a day-clustered (cases of one day summed) sandwich standard error; the plan's 'fewer than the minimum' is reported as not observable.
- Size: unusual move +5.48 % (t 1.90, the cases of one day together: 110 days) per case over 20 bars, 0.233 of the coin's usual move (21.24 %); normal drift in its direction +2.59 %, total +8.07 %; 124 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d`
Measure: `measure.py`
