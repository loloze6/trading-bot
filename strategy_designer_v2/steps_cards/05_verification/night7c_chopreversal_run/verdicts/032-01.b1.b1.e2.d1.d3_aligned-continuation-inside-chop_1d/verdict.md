---
plan: 032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop_1d
idea: 032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 7-bar forward return on the forecast: 0.00123453; OLS slope t: 3.89505 (threshold: slope positive with t >= 2 to confirm (with the supporting check); negative with t <= -2 to reject; at least 30 cases)
- Supporting check: mean drift-adjusted 7-bar return signed by forecast, day-clustered t >= 2: 0.0135488, passed: True
- Counts: cases: 1114, days: 366, active bars: 8133
- Decided by: Confirm: the slope is positive with t >= 2 and the signed drift-adjusted mean is positive with day-clustered t >= 2, over at least 30 cases.
- Reading: ER(30), the 7-day and 30-day returns are recomputed from each window's closes (ER = |close change over 30 bars| / sum of the 30 absolute daily changes); on bars without enough in-window history the detector's 'chop' regime and the sign of the raw scaled_week value stand in; the drift is the coin's mean 7-bar return on all grid bars of all its windows, the slope is a pooled OLS of drift-adjusted return on the forecast with its ordinary t, and the supporting t is a day-clustered t (deviations summed per day, G/(G-1) correction).
- Size: unusual move +1.06 % (t 2.75, the cases of one day together: 1043 days) per case over 7 bars, 0.079 of the coin's usual move (12.44 %); normal drift in its direction -0.03 %, total +1.03 %; 1758 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002943 on the check folds against +0.001235 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop_1d`
Measure: `measure.py`
