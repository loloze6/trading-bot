---
plan: 051-01_falling-agitated-scaled-fall-next-day-rebound_1d
idea: 051-01_falling-agitated-scaled-fall-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move (close[t+1]/close[t]-1 minus coin mean daily return) over bars with forecast > 0: 0.00230916; t of the mean, cases of one day pooled: 0.797151 (threshold: confirm: mean > 0 with t >= 2 and slope > 0 with t >= 2; reject: mean < 0 with t <= -2 or slope < 0 with t <= -2)
- Supporting check: slope of next-day unusual move on forecast (day-pooled t): 0.000477552, passed: False
- Counts: cases: 1404, distinct case days: 444
- Decided by: Inconclusive: neither the confirm nor the reject rule is met.
- Reading: Cases are every bar with forecast > 0 and a next close in the same window, the drift is the coin's mean 1-bar return over all its windows, day pooling uses per-day sums of deviations (mean) or of scores (OLS slope) with a D/(D-1) correction, and the plan's 'fewer than 30 distinct case days' is applied as a minimum count giving 'not observable'.
- Size: unusual move +0.18 % (t 0.52, the cases of one day together: 328 days) per case over 1 bars, 0.037 of the coin's usual move (5.40 %); normal drift in its direction +0.15 %, total +0.33 %; 909 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/051-01_falling-agitated-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/unseen_coins/backtests/051-01_falling-agitated-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
