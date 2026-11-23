---
plan: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of pooled coin-excess 3-bar return on forecast: -0.000797836; OLS slope t: -1.77874 (threshold: confirm if t >= 2 with forecast-weighted mean excess > 0; reject if t <= -2; at least 300 grid cases with forecast > 0)
- Supporting check: forecast-weighted mean excess 3-bar return > 0: -0.00853394, passed: False
- Counts: grid cases with forecast > 0: 243, grid cases: 624
- Decided by: Only 243 grid cases with forecast > 0, below the plan's minimum of 300, so the data could not show the idea.
- Reading: The grid is positions 0, 3, 6, ... of each window, keeping only cases with a full 3-bar forward return inside the window. The coin's mean 3-bar return is taken over all its grid cases across windows. The slope's t is from ordinary least squares on all pooled grid cases, zero forecasts included. Fewer than 300 forecast > 0 cases is reported as 'not observable', following the workflow's rule for minimum counts rather than the plan's 'inconclusive'.
- Size: unusual move +0.68 % (t 0.63, the cases of one day together: 111 days) per case over 3 bars, 0.071 of the coin's usual move (5.48 %); normal drift in its direction +0.02 %, total +0.70 %; 174 cases
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d.md`
Record: `steps_cards/04_backtest/night_006_run/unseen_2026/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d`
Measure: `measure.py`
