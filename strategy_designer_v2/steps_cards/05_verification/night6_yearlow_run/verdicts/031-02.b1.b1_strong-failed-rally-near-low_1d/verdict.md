---
plan: 031-02.b1.b1_strong-failed-rally-near-low_1d
idea: 031-02.b1.b1_strong-failed-rally-near-low
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 20-day move of short cases (return minus drift, short direction): -0.000278416; day-clustered t: -0.00794198 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: 20-day return after largest-third |forecast| minus after smallest third (must be < 0): -0.0639905, passed: True
- Counts: cases: 167, cases on distinct days: 128, supporting check bars: 87
- Decided by: The day-clustered t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The regime part of the situation (distance from the 365-day closing low at or below its median) is read from the recorded `regime` == 'mean_reversion' since the detector's component is not recorded and 365 days cannot be rebuilt from ~120-bar windows, the rally part as a recorded raw 60-day return > 0, the side as short; a case is the first short bet (rise of |forecast| of at least 2 points) in each 20-bar grid cell of a window, the day-clustered t uses the cluster-robust standard error with a G/(G-1) correction, the minimum is the number of distinct days of the cases, and the supporting check's thirds are the top and bottom floor(n/3) grid bars (positions 0, 20, 40, ...) in regime with nonzero forecast, pooled across coins and windows, sorted by |forecast|, on the raw 20-bar return.
- Size: unusual move -0.03 % (t -0.01, the cases of one day together: 128 days) per case over 20 bars, 0.065 of the coin's usual move (21.21 %); normal drift in its direction -3.28 %, total -3.31 %; 167 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-02.b1.b1_strong-failed-rally-near-low_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b1_strong-failed-rally-near-low_1d`
Measure: `measure.py`
