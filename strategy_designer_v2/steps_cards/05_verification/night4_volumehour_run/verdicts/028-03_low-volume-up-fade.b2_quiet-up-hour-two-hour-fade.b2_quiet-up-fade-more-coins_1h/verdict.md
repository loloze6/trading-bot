---
plan: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 2-bar excess return of short bets (vs coin's normal 2-bar drift), before costs: 0.00038021; t of the mean: 3.22493 (threshold: confirm t >= 2 over >= 30 cases with positive slope; reject t <= -2 over >= 30 cases)
- Supporting check: OLS slope of short-direction excess return on forecast size: 1.25646e-05, passed: True
- Counts: cases: 17126
- Decided by: Mean short-direction excess return has t >= 2 over at least 30 cases and the supporting slope is above 0.
- Reading: A bet is a rise of the short forecast's magnitude of at least 2 points from its lowest short level since the last bet (reset to 0 after flat or long), the first bet bar of each non-overlapping 2-bar cell of a window is the case, cases are pooled over all coins for the mean and its ordinary t, the forecast size is its absolute value, and the volume ratio for the situation check is recomputed within each window with a 720-bar mean including the current bar.
- Size: unusual move +0.04 % per case over 2 bars, 0.027 of the coin's usual move (1.47 %); normal drift in its direction -0.01 %, total +0.03 %; 17126 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h`
Measure: `measure.py`
