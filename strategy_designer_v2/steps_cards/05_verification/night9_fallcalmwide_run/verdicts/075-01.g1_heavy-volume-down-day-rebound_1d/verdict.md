---
plan: 075-01.g1_heavy-volume-down-day-rebound_1d
idea: 075-01.g1_heavy-volume-down-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on the forecast, down days, day-pooled: 2.30112; slope t, day-clustered: 2.30112 (threshold: t >= 2 confirms (with top-minus-bottom > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean excess next-day return, top third minus bottom third of forecasts: 0.00363405, passed: True
- Counts: down-day cases: 18171, distinct days: 2398
- Decided by: The slope's t is 2 or more and the top-minus-bottom difference is above 0.
- Reading: Down day = close below the prior close inside the same window (a window's first bar has no prior close in the record and is left out of the check and the measure); the slope's t uses a day-clustered standard error (deviations x residuals summed per day, G/(G-1) correction) so cases on the same day across coins count as one piece of evidence; top and bottom thirds are forecasts at or above the pooled 2/3 quantile and at or below the 1/3 quantile; the minimum is unmet if either fewer than 300 cases or fewer than 150 distinct days.
- Size: unusual move +0.08 % (t 0.69, the cases of one day together: 2141 days) per case over 1 bars, 0.019 of the coin's usual move (5.31 %); normal drift in its direction +0.15 %, total +0.23 %; 12567 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +1.483 on the check folds against +2.301 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/075-01.g1_heavy-volume-down-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.g1_heavy-volume-down-day-rebound_1d`
Measure: `measure.py`
