---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean short-direction unusual 10-bar move, cases forecast <= -2: 0.00856572; t of the mean: 1.46562 (threshold: confirm t >= 2 over >= 30 cases with supporting check > 0; reject t <= -2 over >= 30 cases)
- Supporting check: mean move |forecast| above median minus at or below median: None, passed: False
- Counts: cases: 627, cases_above_median: 0, cases_at_or_below_median: 627, active_bars: 8944
- Decided by: The main-measure t lies between -2 and 2 over at least 30 cases.
- Reading: Situation = close below the SMA50 computed inside the window (the recorded regime 'trending' where fewer than 50 in-window closes exist) and the raw support_cluster value > 0, expected side short; cases are grid cells (positions 0,10,20,... of each window with t+10 in the window) with forecast <= -2, pooled over all coins; drift is the coin's mean 10-bar return on the same grid over all its windows; supporting check splits by |forecast| > median vs <= median.
- Size: unusual move +0.51 % per case over 10 bars, 0.034 of the coin's usual move (14.49 %); normal drift in its direction -1.19 %, total -0.67 %; 943 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d`
Measure: `measure.py`
