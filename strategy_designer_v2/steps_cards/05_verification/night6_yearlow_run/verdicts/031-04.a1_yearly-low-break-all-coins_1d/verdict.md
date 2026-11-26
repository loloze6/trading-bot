---
plan: 031-04.a1_yearly-low-break-all-coins_1d
idea: 031-04.a1_yearly-low-break-all-coins
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move of long cases (return from signal close minus coin's normal 10-bar drift): 0.0684144; t of the mean, cases of one day summed: 1.7793 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; min 30 cases on 20 distinct days)
- Supporting check: mean unusual move of above-median-forecast cases minus below-median-forecast cases > 0: -0.0273968, passed: False
- Counts: cases: 18, distinct days: 16
- Decided by: The plan's minimum of 30 cases on at least 20 distinct days is not reached (18 cases on 16 days).
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest long level since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, cases whose 10-bar return leaves the window are dropped, the t uses a day-clustered standard error with a G/(G-1) correction, and cases with a forecast equal to the median are left out of the supporting check.
- Size: unusual move +6.84 % (t 1.84, the cases of one day together: 16 days) per case over 10 bars, 0.422 of the coin's usual move (15.55 %); normal drift in its direction +1.66 %, total +8.50 %; 18 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-04.a1_yearly-low-break-all-coins_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-04.a1_yearly-low-break-all-coins_1d`
Measure: `measure.py`
