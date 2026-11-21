---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar unusual move in the short direction per bet case: 0.00116072; t of the mean: 0.527992 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half: 0.00478507, passed: True
- Counts: independent cases: 2058
- Decided by: t of the mean unusual move lies between -2 and 2
- Reading: situation taken as raw component > 0 with a negative forecast; a bet is a rise of |forecast| on the short side of >= 2 points from its lowest size since the last bet (reset to 0 when flat or long); each 5-bar grid cell's case is its first bet; the larger half is |forecast| strictly above the median, the smaller half at or below it
- Size: unusual move +0.12 % per case over 5 bars, 0.005 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.47 %; 2058 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d`
Measure: `measure.py`
