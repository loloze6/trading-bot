---
plan: 036-01_scaled-rally-week-continuation_1d
idea: 036-01_scaled-rally-week-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 7-bar unusual move (return minus coin's normal 7-bar drift) per long bet, day-clustered t: -0.0030477; t of the mean, cases of one day summed: -0.671998 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on forecast at signal bar: 0.00088022, passed: True
- Counts: distinct case days: 854, cases: 1757
- Decided by: t between -2 and 2: neither confirm nor reject rule met (inconclusive rule).
- Reading: Cases are long bets (forecast rise >= 2 points from its lowest long level since the last bet, from 0 after flat), the first per 7-bar grid cell of each window, needing close[t+7] in the window; the normal drift is the coin's mean non-overlapping 7-bar return over all its windows; the day-clustered t uses a G/(G-1) correction; the plan's 30-case-day minimum is treated as the minimum count giving 'not observable'.
- Size: unusual move -0.30 % (t -0.67, the cases of one day together: 854 days) per case over 7 bars, -0.024 of the coin's usual move (12.44 %); normal drift in its direction +0.91 %, total +0.60 %; 1757 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/036-01_scaled-rally-week-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/036-01_scaled-rally-week-continuation_1d`
Measure: `measure.py`
