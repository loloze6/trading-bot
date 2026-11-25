---
plan: 058-01.b2_quiet-volume-calm-fall-continues_1d
idea: 058-01.b2_quiet-volume-calm-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (-forecast/10) x 5-bar excess return on grid bars with forecast < 0: -0.00589599; t of the mean, cases of one day taken together: -0.678147 (threshold: confirm: mean > 0 with t >= 2 and check passing; reject: mean < 0 with t <= -2)
- Supporting check: trending grid cases: excess return of quieter half minus heavy-volume (forecast 0) cases < 0: 0.00338858, passed: False
- Counts: grid cases with forecast < 0: 385, days of those cases: 178, heavy-volume cases for the check: 59
- Decided by: The main measure's t is between -2 and 2.
- Reading: The 30-day fall is taken from closes when 30 prior bars exist in the window and from regime 'trending' otherwise; the coin's mean 5-bar return is the mean of its grid returns over all windows; the check's excess return is unweighted and the median is over negative forecasts of trending grid cases; the day-clustered t uses a n_days/(n_days-1) correction.
- Size: unusual move +0.58 % (t 0.86, the cases of one day together: 259 days) per case over 5 bars, 0.056 of the coin's usual move (10.60 %); normal drift in its direction -0.67 %, total -0.08 %; 327 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.b2_quiet-volume-calm-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.b2_quiet-volume-calm-fall-continues_1d`
Measure: `measure.py`
