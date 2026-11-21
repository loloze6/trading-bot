---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
fit: exact
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of -(forecast/10) x drift-adjusted 10-bar return on short grid bars: -0.0117786; t of the mean: -2.29845 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2)
- Supporting check: drift-adjusted 10-bar fall, larger minus smaller |forecast| half (Welch t 1.312): 0.0108844, passed: True
- Counts: non-overlapping grid cases with forecast below 0: 1164, larger-forecast half: 582, smaller-forecast half: 582
- Decided by: The main mean is < 0 with t <= -2: the coin rises beyond its drift after these closes.
- Reading: The grid is positions 0,10,20,... of each window with the 10-bar return kept inside it, the drift is each coin's mean 10-bar return on that grid over all its windows, the larger half is |forecast| strictly above the median (ties go to the smaller half), and the plan's 100-case minimum is applied as 'not observable'.
- Size: unusual move +0.53 % per case over 10 bars, 0.026 of the coin's usual move (14.49 %); normal drift in its direction -1.19 %, total -0.66 %; 1247 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d`
Measure: `measure.py`
