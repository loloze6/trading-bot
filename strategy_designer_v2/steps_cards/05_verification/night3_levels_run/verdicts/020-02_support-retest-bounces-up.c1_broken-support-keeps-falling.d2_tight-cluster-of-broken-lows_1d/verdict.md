---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return on short size (-forecast/10), non-overlapping grid, pooled: -0.00838804; OLS slope t: -3.39633 (threshold: confirm: slope < 0 with t <= -2 (and largest-third mean < 0); reject: slope > 0 with t >= +2)
- Supporting check: mean 5-bar excess return in the largest third of short sizes: -0.00780261, passed: True
- Counts: non-zero-forecast grid cases: 2359, largest-third cases: 786, grid cases in regression: 3419
- Decided by: The slope is negative with t <= -2 and the largest-third mean excess return is below zero.
- Reading: The regression uses every grid bar (zero-forecast bars at short size 0) with the coin's mean taken over all its non-overlapping grid returns, and the largest third is the top floor(n/3) non-zero-forecast grid cases ranked by short size.
- Size: unusual move +0.12 % per case over 5 bars, 0.005 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.47 %; 2058 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d`
Measure: `measure.py`
