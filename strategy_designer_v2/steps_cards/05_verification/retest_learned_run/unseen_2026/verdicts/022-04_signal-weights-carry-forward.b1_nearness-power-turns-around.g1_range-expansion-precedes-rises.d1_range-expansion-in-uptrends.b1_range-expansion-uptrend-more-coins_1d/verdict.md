---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: upper-half minus lower-half mean excess 5-bar return (split at median forecast): 0.00467303; Welch t: 0.57058 (threshold: confirm: difference > 0 with Welch t >= 2 and supporting check; reject: difference < 0 with Welch t <= -2)
- Supporting check: mean excess 5-bar return of upper-half cases > 0: 0.00399922, passed: True
- Counts: cases in upper half: 281, cases in lower half: 281, cases: 562
- Decided by: Welch t lies between -2 and 2.
- Reading: The 20-day return is recomputed as close[t]/close[t-20]-1 inside each window, so active bars of a window's first 20 rows are left out of the agreement; the trending regime for cases is the record's `regime` column; the coin's mean 5-bar return is the mean of all its non-overlapping grid returns over all its windows; the median is taken over all cases of all coins pooled; returns are fractions.
- Size: unusual move +0.74 % per case over 5 bars, 0.074 of the coin's usual move (9.44 %); normal drift in its direction +0.20 %, total +0.94 %; 657 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/unseen_2026/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d`
Measure: `measure.py`
