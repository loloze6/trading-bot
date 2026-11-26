---
plan: 033-02.d1_upside-break-five-day-hold_1d
idea: 033-02.d1_upside-break-five-day-hold
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of long cases: 0.017468; day-clustered t: 2.04949 (threshold: confirm: mean > 0 with t >= 2 on at least 30 case-days; reject: t <= -2 on at least 30 case-days)
- Supporting check: larger-half minus smaller-half mean unusual move (by forecast): 0.0387613, passed: True
- Counts: case-days: 284, cases: 387
- Decided by: Mean unusual move above 0 with t >= 2 on at least 30 case-days, and the larger-half minus smaller-half difference above 0.
- Reading: A case is the first bar in each 5-bar grid cell (from each window's first row) where the long forecast rises by at least 2 points from its lowest level since the last bet, its 5-bar return needing the bar 5 rows later in the same window; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the halves are the lower and upper floor(n/2) cases by forecast rank (ties by time, coin), the middle case left out when n is odd.
- Size: unusual move +1.75 % (t 2.05, the cases of one day together: 284 days) per case over 5 bars, 0.139 of the coin's usual move (10.60 %); normal drift in its direction +0.60 %, total +2.34 %; 387 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01427 on the check folds against +0.01747 on every fold
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-02.d1_upside-break-five-day-hold_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-02.d1_upside-break-five-day-hold_1d`
Measure: `measure.py`
