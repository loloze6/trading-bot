---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
fit: exact
status: inconclusive
---
Situation check: 93 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed unusual 48-bar move per case: 0.0154813; t of the mean: 3.14814 (threshold: mean > 0 with t >= 2 (confirm, with size check); mean < 0 with t <= -2 (reject))
- Supporting check: mean signed unusual move, |forecast| above median minus below median: -0.00252714, passed: False
- Counts: cases: 374, cases above median: 187, cases below median: 187
- Decided by: t >= 2 but the size check (above-median minus below-median |forecast|) fails.
- Reading: Cases are the nonzero-forecast bars with 48 bars ahead in their window, keeping a bar only if 48 bars after the previous kept case; the normal drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; cases with |forecast| equal to the median are left out of the size check; the plan's 30-case minimum maps to 'not observable'.
- Size: unusual move +1.73 % per case over 48 bars, 0.246 of the coin's usual move (6.84 %); normal drift in its direction +0.07 %, total +1.80 %; 332 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h`
Measure: `measure.py`
