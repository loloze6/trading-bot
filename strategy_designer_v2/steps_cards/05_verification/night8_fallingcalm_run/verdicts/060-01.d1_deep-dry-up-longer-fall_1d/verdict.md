---
plan: 060-01.d1_deep-dry-up-longer-fall_1d
idea: 060-01.d1_deep-dry-up-longer-fall
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of short-direction 20-bar excess return on |forecast| (grid cells with forecast < 0): -3.22396e-05; OLS slope t: -0.0152591 (threshold: slope t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; fewer than 30 cells: not observable)
- Supporting check: top third minus bottom third mean short excess return by |forecast|: 0.00491276, passed: True
- Counts: grid cells with a negative forecast: 179
- Decided by: The slope t is between -2 and 2.
- Reading: Falling profile taken as the regime detector's decision (regime 'unknown', i.e. not vetoed to 'chop'), dry-up as raw vol_dryup < 0 and expected side short; grid cells at positions 0,20,40,... of each window with t+20 inside it, coin mean 20-bar return taken over that grid in all its windows, cells pooled over all coins for one OLS slope t, thirds as floor(n/3) cells by |forecast|, and the plan's minimum of 30 cells treated as a minimum count (not observable below it).
- Size: unusual move +3.63 % (t 2.33, the cases of one day together: 189 days) per case over 20 bars, 0.157 of the coin's usual move (21.24 %); normal drift in its direction -2.55 %, total +1.09 %; 239 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-01.d1_deep-dry-up-longer-fall_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-01.d1_deep-dry-up-longer-fall_1d`
Measure: `measure.py`
