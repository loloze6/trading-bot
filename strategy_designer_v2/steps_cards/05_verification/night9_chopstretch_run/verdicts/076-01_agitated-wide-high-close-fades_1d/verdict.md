---
plan: 076-01_agitated-wide-high-close-fades_1d
idea: 076-01_agitated-wide-high-close-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 1-day short-direction unusual move on forecast<0 bars: 0.0029342; t of the mean, deviations summed per day: 1.29098 (threshold: t >= 2 confirms (with supporting difference > 0); t <= -2 rejects)
- Supporting check: unusual move of larger-|forecast| half minus smaller half: 0.00282672, passed: True
- Counts: distinct days of cases: 827, cases: 1450
- Decided by: The t lies between -2 and 2.
- Reading: Cases are every bar with forecast < 0 and a next bar in the same window (the 1-bar grid is every bar), the drift is the coin's mean 1-day return over all its windows, the day-clustered variance uses a D/(D-1) correction, the halves are the top and bottom floor(n/2) cases by |forecast| (middle case dropped if n is odd), and the plan's 30-day minimum maps to 'not observable'.
- Size: unusual move +0.26 % (t 1.05, the cases of one day together: 709 days) per case over 1 bars, 0.066 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.13 %; 1195 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/076-01_agitated-wide-high-close-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/076-01_agitated-wide-high-close-fades_1d`
Measure: `measure.py`
