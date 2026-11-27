---
plan: 067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue_1d
idea: 067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue
fit: adapted
status: mismatch
---
Situation check: 52 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90 % of the active bars are short bars in the plan's situation (60-day return within -10 %..+10 % and 30-day depth <= -2 usual moves).
- Reading: The 60-day return is recomputed from closes inside each window, and on bars where 60 earlier bars are not in the window the detector's regime stands in for it; depth is the recorded raw value of the 'depth' component; any nonzero forecast that is not negative counts as disagreement.
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue_1d`
Measure: `measure.py`
