---
plan: 067-01.b1.b1.b2_choppy-stretch-carry-all-coins_1d
idea: 067-01.b1.b1.b2_choppy-stretch-carry-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (5-bar forward return - coin mean 5-bar return), grid cases: 0.0059144; t of the mean, cases of one day taken together: 0.794109 (threshold: confirm: > 0 with t >= 2 and both sides > 0; reject: < 0 with t <= -2)
- Supporting check: same mean on long and on short cases, each above 0: 0.00466283, passed: True
- Counts: cases: 1641, long cases: 844, short cases: 797, distinct days: 429
- Decided by: The t of the main measure lies between -2 and 2, which the plan calls inconclusive.
- Reading: The choppy profile is read as the detector's regime 'unknown' (the regime that carries the stretch strategy; trend beyond ±10 is vetoed to the flat regime), the expected side as the sign of the raw stretch (close above SMA20 = long); the coin's mean 5-bar return is the mean over all its non-overlapping grid bars of all windows; the day-clustered t sums deviations per UTC day with a D/(D-1) correction; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.28 % (t 0.92, the cases of one day together: 1180 days) per case over 5 bars, 0.014 of the coin's usual move (12.35 %); normal drift in its direction -0.02 %, total +0.26 %; 2315 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01.b1.b1.b2_choppy-stretch-carry-all-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1.b1.b2_choppy-stretch-carry-all-coins_1d`
Measure: `measure.py`
