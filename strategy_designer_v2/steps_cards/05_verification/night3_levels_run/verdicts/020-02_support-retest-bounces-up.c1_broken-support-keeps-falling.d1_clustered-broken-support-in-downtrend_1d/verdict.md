---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar short-side move over short bets: 0.00189583; t of the mean: 0.693574 (threshold: positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 to reject)
- Supporting check: larger-|forecast| half minus smaller half, mean unusual short move: None, passed: None
- Counts: cases: 1355, larger half: 0, smaller half: 1355
- Decided by: Inconclusive: the t of the mean unusual short-side move lies between -2 and 2.
- Reading: Situation = close below its 50-day SMA (recomputed from the window's closes, the recorded regime used on the first 49 bars of a window where the SMA cannot be rebuilt) and a positive raw low_cluster value, expected side short; cases are bets (short forecast magnitude rising >= 2 from its lowest level since the last bet, reset to 0 on flat/long), the first per 5-bar grid cell with a 5-bar return inside the window; the larger half is |forecast| strictly above the cases' median, the smaller half at or below it.
- Size: unusual move +0.19 % per case over 5 bars, 0.013 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.40 %; 1355 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d`
Measure: `measure.py`
