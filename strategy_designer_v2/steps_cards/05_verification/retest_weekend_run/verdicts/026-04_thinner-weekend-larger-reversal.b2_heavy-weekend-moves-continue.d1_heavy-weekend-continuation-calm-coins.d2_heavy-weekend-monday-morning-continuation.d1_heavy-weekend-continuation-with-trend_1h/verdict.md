---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 12-bar move in the forecast's direction: 0.00615464; t of the mean: 2.42457 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: upper minus lower half of |forecast|, mean unusual move: 0.00417881, passed: True
- Counts: cases over all coins and windows: 305, active bars: 309, evaluable active bars: 229
- Decided by: mean unusual move > 0 with t >= 2 and the upper-minus-lower |forecast| half difference is above 0
- Reading: situation bar read as the bar whose close (timestamp + 1h) is Monday 00:00 UTC, with 48/720-bar returns and the 48-vs-prior-120-bar volume ratio rebuilt from in-window prices, active bars lacking that history left out of the agreement share; cases deduplicated to the first nonzero bar per coin per ISO week, and the median split puts |forecast| above the median in the upper half
- Size: unusual move +0.61 % per case over 12 bars, 0.174 of the coin's usual move (3.43 %); normal drift in its direction +0.02 %, total +0.63 %; 277 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h`
Measure: `measure.py`
