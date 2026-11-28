---
plan: 090-01_calm-decline-scaled-push-continues_1d
idea: 090-01_calm-decline-scaled-push-continues
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day forward return minus coin mean 5-day return on raw push: 0.00418319; t of OLS slope, day-clustered SE: 0.888756 (threshold: t of slope >= 2 (with check and >= 100 samples) confirms; <= -2 (>= 100 samples) rejects)
- Supporting check: mean unusual 5-day move of cases (forecast rises >= 2) above 0: 0.00526907, passed: True
- Counts: non-overlapping in-profile samples: 699, cases: 458, days of samples: 294
- Decided by: The slope's t is between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.889 (below 1), 458 cases (30 needed).
- Reading: The falling calm profile is the recorded regime 'unknown' (detector inputs are not recorded and need 365-day history), the drift is the coin's mean non-overlapping 5-day return over all its windows, 'cases on the same day taken together' is a pooled OLS slope with day-clustered standard errors, and cases are the first long bet per 5-bar grid cell of each window.
- Size: unusual move +0.53 % (t 1.04, the cases of one day together: 314 days) per case over 5 bars, 0.051 of the coin's usual move (11.31 %); normal drift in its direction +0.61 %, total +1.14 %; 458 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.889 (below 1), 458 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/090-01_calm-decline-scaled-push-continues_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/090-01_calm-decline-scaled-push-continues_1d`
Measure: `measure.py`
