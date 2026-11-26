---
plan: 061-01.g1_choppy-calm-day-follow-through_1d
idea: 061-01.g1_choppy-calm-day-follow-through
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward excess return on forecast (pooled, non-overlapping grid, forecast != 0): 0.000905422; OLS slope t: 3.06597 (threshold: confirm: slope > 0 with t >= 2 and supporting check > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean of sign(forecast) x excess 5-bar return on grid bars with |forecast| >= 10: 0.0131877, passed: True
- Counts: grid cases with a non-zero forecast: 566, grid cases with |forecast| >= 10: 248
- Decided by: The slope is positive with t >= 2 and the supporting check is above 0 (confirm rule).
- Reading: The plan's choppy calm profile is taken as the bars whose regime is 'unknown' (the detector's non-chop regime) and the expected side as the sign of the day's scaled move (raw component, else the close-to-close return); the coin's mean 5-bar return is the mean over all non-overlapping grid returns of all its windows; the slope is an OLS with intercept; the plan's minimum of 100 grid cases is applied as 'not observable'.
- Size: unusual move +0.46 % (t 1.41, the cases of one day together: 577 days) per case over 5 bars, 0.041 of the coin's usual move (10.60 %); normal drift in its direction +0.01 %, total +0.47 %; 836 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005568 on the check folds against +0.0009054 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1_choppy-calm-day-follow-through_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1_choppy-calm-day-follow-through_1d`
Measure: `measure.py`
