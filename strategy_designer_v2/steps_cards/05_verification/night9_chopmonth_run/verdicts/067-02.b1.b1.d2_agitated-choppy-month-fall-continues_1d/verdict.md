---
plan: 067-02.b1.b1.d2_agitated-choppy-month-fall-continues_1d
idea: 067-02.b1.b1.d2_agitated-choppy-month-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short-side 7-bar excess return: 0.0101563; t of the weighted mean, cases of one day taken together: 0.74424 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: deeper half minus shallower half excess 7-bar return (below 0): -0.0246632, passed: True
- Counts: independent cases (days): 108, cases: 215
- Decided by: The t is between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is the 30-bar return (month_fall raw value, recomputed from closes where missing) below 0 on bars whose regime is the profile's regime 'unknown', short side; independent cases are the distinct UTC days the grid cases fall on; the coin's mean 7-bar return is over all grid bars of all its windows; the halves are the n//2 largest and n//2 smallest |forecast| cases (the median case left out when n is odd) compared on unweighted mean unsigned excess return; a count below 30 is reported as not observable.
- Size: unusual move +1.22 % (t 1.66, the cases of one day together: 265 days) per case over 7 bars, 0.076 of the coin's usual move (12.84 %); normal drift in its direction -0.94 %, total +0.28 %; 359 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.d2_agitated-choppy-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d2_agitated-choppy-month-fall-continues_1d`
Measure: `measure.py`
