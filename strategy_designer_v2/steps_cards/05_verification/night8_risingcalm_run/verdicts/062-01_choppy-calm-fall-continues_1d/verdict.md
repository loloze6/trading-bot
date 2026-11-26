---
plan: 062-01_choppy-calm-fall-continues_1d
idea: 062-01_choppy-calm-fall-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 5-day excess return over the coin's normal drift, forecast < 0 grid bars: 0.00608693; t of the mean, cases of one day summed: 0.968053 (threshold: confirm t >= 2 with larger-half minus smaller-half > 0; reject t <= -2; at least 30 distinct days)
- Supporting check: larger-|forecast| half minus smaller half, mean short excess return: 0.00416795, passed: True
- Counts: cases: 269, distinct days holding cases: 164
- Decided by: t lies between -2 and 2
- Reading: choppy calm profile read as regime 'unknown'; the normal drift is each coin's mean 5-day return on the non-overlapping grid over all its windows; the day-clustered t uses a G/(G-1) correction; the larger half is |forecast| strictly above the median, the smaller half the rest; the plan's 'fewer than 30 distinct days' is treated as a minimum count, giving 'not observable'.
- Size: unusual move +0.38 % (t 0.85, the cases of one day together: 357 days) per case over 5 bars, 0.043 of the coin's usual move (10.60 %); normal drift in its direction -0.62 %, total -0.25 %; 478 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/062-01_choppy-calm-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/062-01_choppy-calm-fall-continues_1d`
Measure: `measure.py`
