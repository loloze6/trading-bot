---
plan: 013-01_nearness-to-high-predicts-gains_1d
idea: 013-01_nearness-to-high-predicts-gains
fit: exact
status: mismatch
---
Situation check: 61 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active bars have a forecast sign equal to the sign of the standardised distance relative to its usual depth (closeness + offset), as the Fidelity's graded closer-than-usual long / farther short rule requires.
- Reading: Expected side taken as sign(closeness + offset) from the recorded standardised values; samples at window positions 0,30,60,90 kept only when t+30 lies in the window; coin mean 30-bar return taken over the same non-overlapping samples of all its windows; OLS slope with intercept; timing gain computed before costs as position after bar t's trade x next-bar coin return, averaged across coins per day then over days.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains_1d`
Measure: `measure.py`
