---
plan: 077-03.d2_low-close-rebound-three-days_1d
idea: 077-03.d2_low-close-rebound-three-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar return of the long bets over the coin's normal 3-bar drift: -0.00394443; t of the mean, cases of one day taken together: -1.07429 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean excess return, top half minus bottom half at the median forecast: 0.0155574, passed: True
- Counts: distinct days with cases: 419, cases: 667
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: Profile read as regime == 'unknown' (the only regime with a strategy, the vetoes send everything else to chop); one case per 3-bar grid cell = the first bet bar in the cell, return taken from that bar's close; normal drift = mean non-overlapping 3-bar grid return of the coin over all its windows; day-clustered t uses summed deviations per day with a D/(D-1) correction; median split: top = forecast above the median, bottom = at or below it; the 30-distinct-days minimum gives 'not observable' as the workflow requires.
- Size: unusual move -0.39 % (t -1.08, the cases of one day together: 419 days) per case over 3 bars, -0.045 of the coin's usual move (8.85 %); normal drift in its direction +0.41 %, total +0.02 %; 667 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03.d2_low-close-rebound-three-days_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.d2_low-close-rebound-three-days_1d`
Measure: `measure.py`
