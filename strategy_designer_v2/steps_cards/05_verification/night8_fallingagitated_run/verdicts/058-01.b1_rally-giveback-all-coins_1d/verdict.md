---
plan: 058-01.b1_rally-giveback-all-coins_1d
idea: 058-01.b1_rally-giveback-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-day move of the cases: 0.0110488; t of the mean, cases of one day summed: 1.7378 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: give-back share, top minus bottom half of raw scaled rise: -0.370567, passed: False
- Counts: distinct days carrying cases: 341, cases: 827, supporting top half cases: 397, supporting bottom half cases: 398
- Decided by: the t of the mean short-direction unusual move lies between -2 and 2
- Reading: the falling agitated profile is read as the detector's regime 'unknown' (both chop vetoes off), since its 60- and 365-bar inputs cannot be rebuilt from the recorded windows; a case is the first short bet (forecast deepening >= 2 points from its lowest short level since the last bet) in each 5-bar cell counted from each window's first row; the t uses a day-clustered standard error with a D/(D-1) factor; the supporting split puts raw values above the median in the top half and the rest in the bottom, leaving out cases whose prior 3-day return is not a rise; the plan's 'fewer than 30 distinct days' is taken as its minimum count, hence 'not observable'.
- Size: unusual move +1.10 % (t 1.74, the cases of one day together: 341 days) per case over 5 bars, 0.087 of the coin's usual move (11.68 %); normal drift in its direction -0.74 %, total +0.36 %; 827 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.b1_rally-giveback-all-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.b1_rally-giveback-all-coins_1d`
Measure: `measure.py`
