---
plan: 028-03_low-volume-up-fade_1h
idea: 028-03_low-volume-up-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 6-bar giveback after short bets, drift removed, signed short, before costs: 0.000217718; t of the mean: 1.20715 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: giveback of larger-|forecast| half minus smaller half: -1.82228e-05, passed: False
- Counts: independent cases across both coins: 12052, cases BTCUSD: 6219, cases ETHUSD: 5833
- Decided by: The main t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The volume gate is read from the recorded regime (mean_reversion = volume ratio 0.5 to 1.5, the detector's components are not recorded) and an up-hour as rise last_history_value > 0; a case is the first short bet (the forecast's magnitude rising by >= 2 points from its lowest short level since the last bet, from 0 after a flat) in each 6-bar grid cell of a window with a full 6-bar return inside the window; the median split puts |forecast| above the median in the larger half and the rest in the smaller half; the plan's 'fewer than 100 independent cases' minimum is reported as not observable.
- Size: unusual move +0.02 % per case over 6 bars, 0.011 of the coin's usual move (1.98 %); normal drift in its direction -0.03 %, total -0.01 %; 12052 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade_1h`
Measure: `measure.py`
