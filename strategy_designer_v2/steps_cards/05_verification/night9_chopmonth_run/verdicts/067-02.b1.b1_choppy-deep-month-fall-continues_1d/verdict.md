---
plan: 067-02.b1.b1_choppy-deep-month-fall-continues_1d
idea: 067-02.b1.b1_choppy-deep-month-fall-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 7-bar forward return on forecast (grid bars with forecast < 0): 0.00271187; OLS slope t, day-clustered: 2.62166 (threshold: confirm: slope > 0 with t >= 2 (and mean short gain > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean short gain (minus drift-adjusted 7-bar return): 0.00661189, passed: True
- Counts: cases: 633, distinct days: 211
- Decided by: The slope is positive with t >= 2 and the mean short gain is above 0, with at least 100 cases on 60 days.
- Reading: The choppy market is read as the detector's regime 'unknown' (the 60-bar move within +-10, the only regime with a strategy) and the fall as a negative 30-bar raw value; the normal 7-bar drift is the coin's mean 7-bar return on the non-overlapping grid of all its windows; pooling cases of the same day is done with a day-clustered standard error of the OLS slope; and the plan's 'fewer than 100 cases or 60 days' is reported as not observable.
- Size: unusual move +1.13 % (t 2.08, the cases of one day together: 624 days) per case over 7 bars, 0.071 of the coin's usual move (14.34 %); normal drift in its direction -1.13 %, total -0.01 %; 1024 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003125 on the check folds against +0.002712 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1_choppy-deep-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1_choppy-deep-month-fall-continues_1d`
Measure: `measure.py`
