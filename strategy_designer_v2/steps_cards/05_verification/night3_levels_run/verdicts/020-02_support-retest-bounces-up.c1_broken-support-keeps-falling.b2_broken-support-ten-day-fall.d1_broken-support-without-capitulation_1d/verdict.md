---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of forecast/10 x (10-bar return minus coin's mean 10-bar return), before costs: 0.0152772; t of the mean: 2.8124 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject))
- Supporting check: mean signed excess return, upper half of |forecast| minus lower half: 0.0285738, passed: True
- Counts: non-zero grid cases: 1164, upper half cases: 582, lower half cases: 582
- Decided by: The mean is above 0 with t >= 2 over at least 30 cases, and the upper half of |forecast| earns more than the lower half.
- Reading: The coin's mean 10-bar return is taken over all grid cells (0, 10, 20, ... of each window, return inside the window) of all its windows; the upper half of |forecast| is the cells strictly above its median and the lower half those at or below; the regime side is read from the recorded `regime` column.
- Size: unusual move +0.49 % per case over 10 bars, 0.023 of the coin's usual move (14.49 %); normal drift in its direction -0.67 %, total -0.18 %; 1207 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d`
Measure: `measure.py`
