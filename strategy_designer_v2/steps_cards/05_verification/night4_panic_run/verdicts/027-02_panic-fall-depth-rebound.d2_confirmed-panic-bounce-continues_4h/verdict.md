---
plan: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h
idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues
fit: adapted
status: inconclusive
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 84-bar forward return minus normal drift on the forecast at the case bar: 0.000655297; OLS slope t: 1.23788 (threshold: confirm: slope > 0 with t >= 2 over >= 30 independent cases; reject: slope < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess 84-bar return of positive-forecast cases above 0: 0.00723387, passed: True
- Counts: independent cases: 797, cases with positive forecast: 471
- Decided by: The slope's t lies between -2 and 2 (or its sign disagrees with its t threshold), which the plan calls inconclusive.
- Reading: The expected side is the sign of the 24h bounce (the Fidelity's graded comparison: larger bounce, higher return), the panic value is rebuilt from prices as (fall / mean |6-bar return| over 180 bars) x (6-bar range / its 180-bar mean) for the stretch ending 6 bars back, using the recorded regime where the window's history is too short; a case is the first bet of each 84-bar grid cell of a window, pooled over all coins, with the normal drift being the coin's mean non-overlapping 84-bar return over all its windows.
- Size: unusual move +1.32 % per case over 84 bars, 0.057 of the coin's usual move (17.66 %); normal drift in its direction +0.42 %, total +1.74 %; 797 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h`
Measure: `measure.py`
