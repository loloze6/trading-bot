---
plan: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d
idea: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean excess 5-bar short return over grid cases with forecast < 0: 0.0101853; t of the mean, cases of one day summed: 1.67701 (threshold: confirm: mean > 0 with t >= 2 (day-clustered) and larger-gap half beats smaller-gap half; reject: mean < 0 with t <= -2)
- Supporting check: larger-gap half minus smaller-gap half mean excess short return: -0.000689084, passed: False
- Counts: grid cases: 721, distinct days with a case: 352
- Decided by: t is between -2 and 2.
- Reading: Choppy bars are read from the recorded regime 'unknown' (the detector's default when the 60-bar evolution is within +/-10), the gap from last_history_value (recomputed from closes where missing); the coin's mean 5-bar return is over all its windows' non-overlapping grid returns; the t uses per-day summed deviations of the weighted values (with D/(D-1) correction); the larger-gap half is |forecast| strictly above the median and the halves compare unweighted mean excess short returns; too few cases gives 'not observable' as the workflow requires.
- Size: unusual move +0.61 % (t 1.87, the cases of one day together: 679 days) per case over 5 bars, 0.070 of the coin's usual move (10.60 %); normal drift in its direction -0.57 %, total +0.04 %; 929 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d`
Measure: `measure.py`
