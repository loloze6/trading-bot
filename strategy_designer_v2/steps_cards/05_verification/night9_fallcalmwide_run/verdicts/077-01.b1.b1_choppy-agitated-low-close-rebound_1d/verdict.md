---
plan: 077-01.b1.b1_choppy-agitated-low-close-rebound_1d
idea: 077-01.b1.b1_choppy-agitated-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return on forecast > 0 bars (coin's next-day return minus coin's mean daily return): 0.00344711; t of the mean, same-day cases combined: 1.04904 (threshold: confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2)
- Supporting check: excess return, forecast above median minus below median (Welch): 0.00294402, passed: True
- Counts: cases: 408, distinct days: 276
- Decided by: The t of the mean excess next-day return lies between -2 and 2: inconclusive.
- Reading: The 20-day mean range includes the current bar and is computed inside each window, so a window's first 19 bars cannot be checked and are left out of the situation check; the close is in the lower half when (close-low)/(high-low) < 0.5; the coin's mean daily return is over every within-window next-day return of all its windows; same-day cases are combined by summing their deviations per UTC day (clustered standard error); the supporting split uses the median forecast of all cases with a next-day return, strictly above versus strictly below it; the plan's 'fewer than 100 cases / 60 days' rule is reported as 'not observable'.
- Size: unusual move +0.37 % (t 1.12, the cases of one day together: 244 days) per case over 1 bars, 0.076 of the coin's usual move (5.33 %); normal drift in its direction +0.13 %, total +0.50 %; 346 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-01.b1.b1_choppy-agitated-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-01.b1.b1_choppy-agitated-low-close-rebound_1d`
Measure: `measure.py`
