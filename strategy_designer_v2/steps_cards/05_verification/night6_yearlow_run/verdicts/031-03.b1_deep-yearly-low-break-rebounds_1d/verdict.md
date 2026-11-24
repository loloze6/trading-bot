---
plan: 031-03.b1_deep-yearly-low-break-rebounds_1d
idea: 031-03.b1_deep-yearly-low-break-rebounds
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move per case over 10 bars (return from signal close minus coin's normal 10-bar drift): 0.0714982; t of the mean, cases of one day taken together: 1.41036 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2; else inconclusive; at least 30 distinct case days)
- Supporting check: mean unusual move of cases with forecast above the median case forecast minus those at or below: 0.0200137, passed: True
- Counts: distinct case days: 12, cases: 13
- Decided by: Fewer than 30 distinct case days pooled over all coins and windows (12), the plan's minimum.
- Reading: A case is the first bet (forecast rise of at least 2 points on its side) in each 10-bar grid cell of a window, dropped when its 10-bar return would leave the window; the normal drift is the coin's mean non-overlapping 10-bar return over all its windows; the plan's 'count under 30 distinct case days' is applied as the minimum count giving 'not observable'.
- Size: unusual move +7.15 % (t 1.47, the cases of one day together: 12 days) per case over 10 bars, 0.450 of the coin's usual move (14.49 %); normal drift in its direction +1.85 %, total +9.00 %; 13 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-03.b1_deep-yearly-low-break-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-03.b1_deep-yearly-low-break-rebounds_1d`
Measure: `measure.py`
