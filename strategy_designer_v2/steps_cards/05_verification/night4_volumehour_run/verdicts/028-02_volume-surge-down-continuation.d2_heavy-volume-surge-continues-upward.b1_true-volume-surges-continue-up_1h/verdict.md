---
plan: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h
idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 4-bar return per bet case (coin drift removed): -0.000136742; t of the mean: -0.837453 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: forecast-weighted mean excess 4-bar return > 0: -5.74695e-05, passed: False
- Counts: cases: 13276
- Decided by: -2 < t < 2 over at least 30 cases: neither the confirm nor the reject rule is met.
- Reading: Situation bars are those whose raw component value is positive (an up hour on traded volume), long side; a bet is a rise of a positive forecast of at least 2 points from its lowest positive level since the last bet (from 0 after a flat), the first bet bar of each non-overlapping 4-bar cell counted from each window's first row is the case, cells whose signal bar lacks 4 later bars in the window are left out, and the coin's drift is the mean 4-bar return on the same grid over all its windows.
- Size: unusual move -0.01 % per case over 4 bars, -0.009 of the coin's usual move (1.62 %); normal drift in its direction +0.02 %, total +0.01 %; 13276 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h`
Measure: `measure.py`
