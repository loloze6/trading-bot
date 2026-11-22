---
plan: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h
idea: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move after bets (long, minus normal drift, before costs): 0.00028103; t of the mean: 2.37574 (threshold: mean > 0 with t >= 2 on at least 30 cases (confirm); mean < 0 with t <= -2 on at least 30 cases (reject))
- Supporting check: mean unusual move, top minus bottom half by volume ratio: 1.10691e-05, passed: True
- Counts: cases: 14913, cases with a volume ratio: 11101, top half: 5550, bottom half: 5550
- Decided by: The mean unusual move is above 0 with t >= 2 on at least 30 cases and the high-minus-low volume split is positive.
- Reading: A case is the first bet bar (long forecast rising >= 2 points from its lowest level since the last bet) in each non-overlapping 2-bar cell from each window's first row, with its 2-bar return inside the window; the normal drift is the coin's mean 2-bar return on the same grid over all its windows; the volume ratio is volume over the trailing 720-bar mean including the bar, computed within the window (cases without 720 bars of history left out of the split), and cases exactly at the median are left out of both halves.
- Size: unusual move +0.03 % per case over 2 bars, 0.025 of the coin's usual move (1.16 %); normal drift in its direction +0.01 %, total +0.04 %; 14913 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h`
Measure: `measure.py`
