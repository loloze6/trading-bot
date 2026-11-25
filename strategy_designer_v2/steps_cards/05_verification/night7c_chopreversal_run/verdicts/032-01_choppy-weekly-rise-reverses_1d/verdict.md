---
plan: 032-01_choppy-weekly-rise-reverses_1d
idea: 032-01_choppy-weekly-rise-reverses
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed 7-bar unusual move (return minus coin's normal 7-bar drift): -0.0109664; t of the mean, cases of one day taken together: -0.994143 (threshold: confirm t >= 2 with rank correlation > 0; reject t <= -2; else inconclusive)
- Supporting check: Spearman rank correlation of |forecast| with short-signed unusual move: -0.0517844, passed: False
- Counts: cases: 400, distinct days: 175
- Decided by: The t of the mean short-signed unusual move lies between -2 and 2.
- Reading: The situation is read as bars the detector labels mean_reversion (its rules are er <= 0.3 and vp >= 0.5, the Fidelity's thresholds; the detector's components are not recorded and the 365-day percentile cannot be rebuilt from 120-bar windows) with a positive scaled 7-day rise (raw value, or the 7-day price return where missing), expected side short; cases are grid bars 0,7,14,... per window with forecast < 0 and a full 7-bar return inside the window; drift is the coin's mean 7-bar return on the same grid over all its windows; the t uses a day-clustered standard error with a G/(G-1) correction; the plan's 'fewer than 30 cases or days' rule is treated as a minimum count (not observable).
- Size: unusual move -0.31 % (t -0.46, the cases of one day together: 448 days) per case over 7 bars, -0.031 of the coin's usual move (12.44 %); normal drift in its direction -0.95 %, total -1.27 %; 671 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01_choppy-weekly-rise-reverses_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01_choppy-weekly-rise-reverses_1d`
Measure: `measure.py`
