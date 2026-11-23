---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed 12-bar excess return, top fifth of |forecast| cases: 0.00463861; t of the mean: 2.44701 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 100 top-fifth cases)
- Supporting check: top-fifth mean minus bottom-fifth mean > 0: 0.0042, passed: True
- Counts: cases: 2395, cases in the top fifth: 479, cases in the bottom fifth: 479
- Decided by: The main mean is positive with t >= 2 and the top-minus-bottom fifth difference is above 0.
- Reading: Situation bars are those starting Sunday 23:00 UTC, side from the sign of the raw component (48-bar price return where not recorded); cases are trending bars with nonzero forecast, first one per coin and calendar date, with a 12-bar return inside their window; the top/bottom fifth are the floor(N/5) cases with the largest/smallest |forecast| pooled over coins, ties broken by coin and time; the coin mean is over grid bars 0,12,24,... of every window.
- Size: unusual move +0.57 % per case over 12 bars, 0.168 of the coin's usual move (3.43 %); normal drift in its direction +0.02 %, total +0.59 %; 385 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h`
Measure: `measure.py`
