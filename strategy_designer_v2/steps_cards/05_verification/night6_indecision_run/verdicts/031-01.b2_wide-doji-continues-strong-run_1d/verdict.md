---
plan: 031-01.b2_wide-doji-continues-strong-run_1d
idea: 031-01.b2_wide-doji-continues-strong-run
fit: adapted
status: mismatch
---
Situation check: 80 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of bars with a non-zero forecast are long bars where the 5-day return > 0, range >= 1.5x the 20-day mean range and flatness >= 0.9 hold
- Reading: Situation recomputed per window from prices (5-bar close change, or the recorded run5_size raw value where present; range over the 20-bar mean range including bar t; 1 - |close-open|/range), active bars with too little in-window history counted as not agreeing; cases are long bets (forecast rise >= 2 points from its low since the last bet, from 0 after flat), the first per 3-bar grid cell, needing 3 bars ahead in the window; case-days are distinct UTC days with a case; t uses day-summed deviations with a G/(G-1) correction; the slope is an OLS of unusual move on the signal bar's forecast.
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b2_wide-doji-continues-strong-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b2_wide-doji-continues-strong-run_1d`
Measure: `measure.py`
