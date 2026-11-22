---
plan: 026-04_thinner-weekend-larger-reversal_1h
idea: 026-04_thinner-weekend-larger-reversal
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 48-bar return minus drift on forecast, signal bars pooled: -2.29393e-05; OLS slope t: -0.189353 (threshold: t >= 2 confirms (with mean unusual move > 0), t <= -2 rejects, otherwise inconclusive; at least 300 signal bars)
- Supporting check: mean unusual move in signal direction > 0: -0.00273383, passed: False
- Counts: signal bars with a nonzero forecast: 2411, signal bars with a nonzero forecast (before return availability): 2451
- Decided by: The slope's t lies between -2 and 2.
- Reading: Signal bars are the Sunday bars whose next bar starts on or after Monday 00:00 UTC with a nonzero forecast; the 48-bar return is close[t+48]/close[t]-1 by row inside the window, the drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows, the slope is OLS with an intercept, and the count of 300 is of signal bars with a nonzero forecast and a full 48-bar return.
- Size: unusual move -0.29 % per case over 48 bars, -0.040 of the coin's usual move (6.56 %); normal drift in its direction -0.02 %, total -0.31 %; 2145 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-04_thinner-weekend-larger-reversal_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal_1h`
Measure: `measure.py`
