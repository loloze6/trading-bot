---
plan: 061-01.d2_rising-calm-up-day-continuation_1d
idea: 061-01.d2_rising-calm-up-day-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar forward return on forecast (forecast > 0, grid cases): 0.00156373; t of slope, day-clustered: 1.54843 (threshold: slope > 0 with day-clustered t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects)
- Supporting check: mean excess 5-bar return, upper half minus lower half of forecasts: 0.0155604, passed: True
- Counts: grid cases with a positive forecast: 337, days: 176
- Decided by: The slope has |t| < 2.
- Reading: Profile from the recorded regime ('unknown' = not vetoed); coin mean = mean of its non-overlapping 5-bar grid returns over all windows; t is the OLS slope over a day-clustered (CR1, G/(G-1)) standard error; halves are the lower and upper n//2 cases sorted by forecast (middle case dropped if n is odd); the plan's 'fewer than 100 cases' minimum is reported as not observable.
- Size: unusual move +0.96 % (t 1.84, the cases of one day together: 444 days) per case over 5 bars, 0.087 of the coin's usual move (10.60 %); normal drift in its direction +0.63 %, total +1.59 %; 696 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.d2_rising-calm-up-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.d2_rising-calm-up-day-continuation_1d`
Measure: `measure.py`
