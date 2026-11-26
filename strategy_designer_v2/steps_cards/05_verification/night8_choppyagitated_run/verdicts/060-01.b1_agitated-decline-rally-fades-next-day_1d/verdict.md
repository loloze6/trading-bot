---
plan: 060-01.b1_agitated-decline-rally-fades-next-day_1d
idea: 060-01.b1_agitated-decline-rally-fades-next-day
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual move over the next 1 bar: 0.00517908; t of the mean, cases of one day together: 2.34883 (threshold: confirm: > 0 with t >= 2 (and slope > 0); reject: < 0 with t <= -2)
- Supporting check: OLS slope of short-direction unusual move on abs(forecast): 0.000134197, passed: True
- Counts: cases: 2538, distinct days: 758
- Decided by: The main measure is above 0 with t >= 2 and the slope on abs(forecast) is above 0.
- Reading: Profile bars are read from the recorded regime ('unknown', the regime left when neither 'chop' veto fires) and up days from the raw scaled rise > 0; cases are every active bar with a next-bar return in its window, the coin's mean is over all its 1-bar returns in all windows, and the day-clustered t uses se = sqrt(G/(G-1) * sum over days of (summed deviations)^2) / n.
- Size: unusual move +0.56 % (t 2.09, the cases of one day together: 565 days) per case over 1 bars, 0.113 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.42 %; 1669 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003485 on the check folds against +0.005179 on every fold
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-01.b1_agitated-decline-rally-fades-next-day_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-01.b1_agitated-decline-rally-fades-next-day_1d`
Measure: `measure.py`
