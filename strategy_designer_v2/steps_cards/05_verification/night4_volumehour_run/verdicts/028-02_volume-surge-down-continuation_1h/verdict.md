---
plan: 028-02_volume-surge-down-continuation_1h
idea: 028-02_volume-surge-down-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 6-bar unusual fall after a short bet (drift removed, sign flipped): -0.000239674; t of the mean: -1.13042 (threshold: mean > 0 with t >= 2 over at least 30 pooled cases to confirm; t <= -2 to reject)
- Supporting check: Spearman rank correlation of signal-hour volume ratio with unusual fall: 0.00602002, passed: True
- Counts: cases: 11303, cases_with_volume_ratio: 8416
- Decided by: t lies between -2 and 2 over at least 30 cases.
- Reading: A case is the first short bet (forecast more negative by >= 2 from its least-short level since the last bet, reset at flat) in each 6-bar grid cell of a window, the drift is the coin's mean 6-bar grid return over all its windows, and the volume ratio is recomputed as volume over its trailing 720-bar mean including the bar, within the window, with cases lacking 720 bars of history left out of the correlation only.
- Size: unusual move -0.02 % per case over 6 bars, -0.012 of the coin's usual move (1.98 %); normal drift in its direction -0.03 %, total -0.06 %; 11303 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation_1h`
Measure: `measure.py`
